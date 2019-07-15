package safefile

import (
	"github.com/pkg/errors"
	"io"
	"os"
	"sync"
)

// 并发安全的对一个文件同时进行读写操作 From: GO并发编程实战 5.1.3
type SafeFile interface {
	// 读一个数据块
	Read() (rsn int64, d Data, err error)
	// 写一个数据块
	Write(d Data) (wsn int64, err error)
	// 获取最后读取的数据块的序列号
	RSN() int64
	// 获取最后写入的数据块的序列号
	WSN() int64
	// 获取数据块的长度
	BlockLen() uint32
	// 关闭数据文件
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

	sf := &safeFile{
		f:        f,
		blockLen: length,
	}

	sf.rcond = sync.NewCond(sf.fmutex.RLocker())
	return sf, nil
}

type safeFile struct {
	f      *os.File
	fmutex sync.RWMutex // 用于文件的读写锁
	// 数据文件的写操作和读操作需要各自独立,因此需要两个字段来存储两类操作的进度
	woffset  int64      // 写操作的偏移量
	roffset  int64      // 读操作的偏移量
	wmutex   sync.Mutex // 写操作需要用到的互斥锁
	rmutex   sync.Mutex // 度小左需要用到的互斥所
	rcond    *sync.Cond // 条件变量
	blockLen uint32     // 一个数据块长度
}

// Read implement SafeFile's Read function
func (s *safeFile) Read() (int64, Data, error) {
	// 更新文件的读偏移量
	s.rmutex.Lock()
	offset := s.roffset
	rsn := offset / int64(s.blockLen) // 序列号
	s.roffset += int64(s.blockLen)
	s.rmutex.Unlock()

	// 读取数据块
	s.fmutex.RLock()
	defer s.fmutex.RUnlock()

	data := make([]byte, s.blockLen)
	for {
		s.fmutex.RLock()
		_, err := s.f.ReadAt(data, offset)
		if err != nil {
			if err != io.EOF {
				s.rcond.Wait()
				// 如果是读取到了文件末尾,就继续读
				continue
			}
			// 即使发生了错误,也应该返回读取的数据块序列号和已经读取的数据
			return rsn, data, err
		}

		return rsn, data, err
	}
}

// Write implement SafeFile's Write function
func (s *safeFile) Write(d Data) (int64, error) {
	// 更新文件的写偏移量
	s.wmutex.Lock()
	offset := s.woffset
	s.woffset += int64(s.blockLen)
	s.wmutex.Unlock()

	// 写入一个数据块
	wsn := offset / int64(s.blockLen)
	data := make([]byte, s.blockLen)
	data = d
	if len(d) > int(s.blockLen) {
		data = d[0:s.blockLen]
	}

	s.fmutex.Lock()
	defer s.fmutex.Unlock()

	_, err := s.f.Write(data)
	if err != nil {
		return wsn, err
	}

	s.rcond.Signal()
	return wsn, nil
}

// RSN implement SafeFile's RSN function
func (s *safeFile) RSN() int64 {
	s.rmutex.Lock()
	defer s.rmutex.Unlock()
	return s.roffset / int64(s.blockLen)
}

// WSN implement SafeFile's WSN function
func (s *safeFile) WSN() int64 {
	s.wmutex.Lock()
	defer s.wmutex.Unlock()
	return s.woffset / int64(s.blockLen)
}

// DataLen implement SafeFile's DataLen function
func (s *safeFile) BlockLen() uint32 {
	return s.blockLen
}

// Close implement SafeFile's Close function
func (s *safeFile) Close() error {
	return s.f.Close()
}
