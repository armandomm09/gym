package cmd

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"

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

func killLabelStudio() error {

	cmd := exec.Command("sh", "-c", "ps aux | grep label-studio | grep -v grep")
	out, err := cmd.Output()
	if err != nil {
		return fmt.Errorf("error al listar procesos: %w", err)
	}

	scanner := bufio.NewScanner(bytes.NewReader(out))
	for scanner.Scan() {
		line := scanner.Text()

		fields := strings.Fields(line)
		if len(fields) < 2 {
			continue
		}
		pid := fields[1]

		killCmd := exec.Command("kill", pid)
		if err := killCmd.Run(); err != nil {
			log.Printf("No se pudo matar PID %s: %v", pid, err)
		} else {
			fmt.Printf("Proceso label‑studio detenido (PID=%s)\n", pid)
		}
	}
	if err := scanner.Err(); err != nil {
		return fmt.Errorf("error leyendo salida: %w", err)
	}
	return nil
}

func execute_python_script(args ...string) {

	comand := exec.Command("python/.venv/bin/python3", args...)

	stdoutPipe, err := comand.StdoutPipe()
	if err != nil {
		log.Fatalf("Error al obtener stdout: %v", err)
	}

	stderrPipe, err := comand.StderrPipe()
	if err != nil {
		log.Fatalf("Error al obtener stderr: %v", err)
	}

	if err := comand.Start(); err != nil {
		log.Fatalf("Error al iniciar el comando: %v", err)
	}

	go func() {
		scanner := bufio.NewScanner(stdoutPipe)
		for scanner.Scan() {
			fmt.Printf("%s\n", scanner.Text())
		}
	}()

	go func() {
		scanner := bufio.NewScanner(stderrPipe)
		for scanner.Scan() {
			if strings.Contains(scanner.Text(), "Looking for locale") || strings.Contains(scanner.Text(), "Provider `faker.providers.") {
				continue
			}
			fmt.Printf("%s\n", scanner.Text())
		}
	}()

	if err := comand.Wait(); err != nil {
		log.Fatalf("Error al esperar el comando: %v", err)
	}

}
