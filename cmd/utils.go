package cmd

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"

	"gopkg.in/yaml.v3"
)

func getConfig() Config {
	yamlData, err := os.ReadFile("config.yaml")
	if err != nil {
		log.Fatalf("Error al leer config.yaml: %v", err)
	}

	var c Config
	if err := yaml.Unmarshal(yamlData, &c); err != nil {
		log.Fatalf("Error al parsear YAML: %v", err)
	}
	return c

}

func execute_python_script(args ...string) {

	comand := exec.Command("python/.venv/bin/python3", args...)
	stdout, err := comand.StdoutPipe()
	if err != nil {
		log.Fatalln("Error executing comand")
	}

	// start the command after having set up the pipe
	if err := comand.Start(); err != nil {
		log.Fatalln("Error executing comand")
	}

	// read command's stdout line by line
	in := bufio.NewScanner(stdout)

	for in.Scan() {
		fmt.Println(in.Text())
	}
}
