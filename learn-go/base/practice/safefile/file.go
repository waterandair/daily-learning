package safefile

import (
	"github.com/pkg/errors"
	"os"
	"sync"
)

// 并发安全的文件读写操作 From: GO并发编程实战 5.1.3
type SafeFile interface {
	Read() (rsn int64, d Data, err error)
	Write(d Data) (wsn int64, err error)
	RSN() int64
	WSN() int64
	DataLen() uint32
	Close() error
}

type Data []byte

func NewSafeFile(path string, length uint32) (SafeFile, error) {
	f, err := os.Create(path)
	if err != nil {
		return nil, err
	}

	if length == 0 {
		return nil, errors.New("Invalid data length!")
	}

	return &safeFile{
		f:   f,
		len: length,
	}, nil
}

type safeFile struct {
	f      *os.File
	fmutex sync.RWMutex // 用于文件的读写锁
	// 数据文件的写操作和读操作需要各自独立,因此需要两个字段来存储两类操作的进度
	woffset int64      // 写操作的偏移量
	roffset int64      // 读操作的偏移量
	wmutex  sync.Mutex // 写操作需要用到的互斥锁
	rmutex  sync.Mutex // 度小左需要用到的互斥所
	len     uint32     // 数据库长度
}
