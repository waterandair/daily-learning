package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/golang/protobuf/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"io"
	"io/ioutil"
	"log"
	"math"
	"net"
	"route_guide/routeguide"
	"route_guide/testdata"
	"sync"
	"time"
)

var (
	tls        = flag.Bool("tls", false, "Connection uses TLS if true, else plain TCP")
	certFile   = flag.String("cert_file", "", "The TLS cert file")
	keyFile    = flag.String("key_file", "", "The TLS key file")
	jsonDBFile = flag.String("json_db_file", "testdata/route_guide_db.json", "A json file containing a list of features")
	port       = flag.Int("port", 10000, "The server port")
)

type routeGuideServer struct {
	savedFeatures []*routeguide.Feature  // read-only after initialized
	mu	sync.Mutex	// protects routeNotes
	routeNotes map[string][]*routeguide.RouteNote
}

func (s *routeGuideServer) GetFeature(ctx context.Context, point *routeguide.Point) (*routeguide.Feature, error) {
	for _, feature := range s.savedFeatures {
		if proto.Equal(feature.Location, point) {
			return feature, nil
		}
	}

	return &routeguide.Feature{Location:point}, nil
}

// 服务端流模式
func (s *routeGuideServer) ListFeature(rect *routeguide.Rectangle, stream routeguide.RouteGuide_ListFeatureServer) error {
	for _, feature := range s.savedFeatures {
		if inRange(feature.Location, rect) {
			if err := stream.Send(feature); err != nil {
				return err
			}
		}
	}
	return nil
}

// 客户端流模式， 计算总 point， feature，总距离， 运算的总时间
func (s *routeGuideServer) RecordRoute(stream routeguide.RouteGuide_RecordRouteServer) error {
	var pointCount, featureCount, distance int32
	var lastPoint *routeguide.Point
	startTime := time.Now()
	for {
		point, err := stream.Recv()
		if err == io.EOF {	// 一次流结束
			endTime := time.Now()
			return stream.SendAndClose(&routeguide.RouteSummary{
				PointCount: pointCount,
				FeatureCount: featureCount,
				Distance: distance,
				ElapsedTime: int32(endTime.Sub(startTime).Seconds()),
			})
		} else if err != nil {
			return err
		} else {
			pointCount ++
			for _, feature := range s.savedFeatures {
				if proto.Equal(feature.Location, point) {
					featureCount ++
				}
			}

			if lastPoint != nil {
				distance += calcDistance(lastPoint, point)
			}

			lastPoint = point
		}
	}
}

// 双流模式
func (s *routeGuideServer) RouteChat(stream routeguide.RouteGuide_RouteChatServer) error {
	for {
		in, err := stream.Recv()
		if err == io.EOF {
			return nil
		} else if err != nil {
			return nil
		} else {
			key := serialize(in.Location)
			s.mu.Lock()
			s.routeNotes[key] = append(s.routeNotes[key], in)

			rn := make([]*routeguide.RouteNote, len(s.routeNotes[key]))
			copy(rn, s.routeNotes[key])
			s.mu.Unlock()

			for _, note := range rn {
				if err := stream.Send(note); err != nil {
					return err
				}
			}
		}
	}
}

func serialize(point *routeguide.Point) string {
	return fmt.Sprintf("%d %d", point.Latitude, point.Longitude)
}


// 返回在指定区域内的坐标点
func inRange(point *routeguide.Point, rect *routeguide.Rectangle) bool {
	left := math.Min(float64(rect.Lo.Longitude), float64(rect.Hi.Longitude))
	right := math.Max(float64(rect.Lo.Longitude), float64(rect.Hi.Longitude))
	top := math.Max(float64(rect.Lo.Latitude), float64(rect.Hi.Latitude))
	bottom := math.Min(float64(rect.Lo.Latitude), float64(rect.Hi.Latitude))
	if float64(point.Longitude) >= left &&
		float64(point.Longitude) <= right &&
		float64(point.Latitude) >= bottom &&
		float64(point.Latitude) <= top {
		return true
	}
	return false
}

// 计算两个经纬度坐标点之间的距离
func calcDistance(p1 *routeguide.Point, p2 *routeguide.Point) int32 {
	const CordFactor float64 = 1e7
	const R float64 = float64(6371000) // earth radius in metres
	lat1 := toRadians(float64(p1.Latitude) / CordFactor)
	lat2 := toRadians(float64(p2.Latitude) / CordFactor)
	lng1 := toRadians(float64(p1.Longitude) / CordFactor)
	lng2 := toRadians(float64(p2.Longitude) / CordFactor)
	dlat := lat2 - lat1
	dlng := lng2 - lng1

	a := math.Sin(dlat/2)*math.Sin(dlat/2) +
		math.Cos(lat1)*math.Cos(lat2)*
			math.Sin(dlng/2)*math.Sin(dlng/2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))

	distance := R * c
	return int32(distance)
}

func toRadians(num float64) float64 {
	return num * math.Pi / float64(180)
}


// loadFeatures loads features from a JSON file.
func (s *routeGuideServer) loadFeatures(filePath string) {
	file, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatalf("Failed to load default features: %v", err)
	}
	if err := json.Unmarshal(file, &s.savedFeatures); err != nil {
		log.Fatalf("Failed to load default features: %v", err)
	}
}


func newServer() *routeGuideServer {
	s := &routeGuideServer{routeNotes: make(map[string][]*routeguide.RouteNote)}
	s.loadFeatures(*jsonDBFile)
	return s
}


func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	var opts []grpc.ServerOption
	if *tls {
		if *certFile == "" {
			*certFile = testdata.Path("server1.pem")
		}
		if *keyFile == "" {
			*keyFile = testdata.Path("server1.key")
		}
		creds, err := credentials.NewServerTLSFromFile(*certFile, *keyFile)
		if err != nil {
			log.Fatalf("Failed to generate credentials %v", err)
		}
		opts = []grpc.ServerOption{grpc.Creds(creds)}
	}
	grpcServer := grpc.NewServer(opts...)
	routeguide.RegisterRouteGuideServer(grpcServer, newServer())
	grpcServer.Serve(lis)
}
