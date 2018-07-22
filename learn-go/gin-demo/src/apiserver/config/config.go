package config


type Config struct {
	Name string
}

func Init(cfg string) error {
	c := Config{
		Name: cfg,
	}

	// 初始化配置文件

	return nil
}

func (c *Config) initConfig() error {

	return nil
}