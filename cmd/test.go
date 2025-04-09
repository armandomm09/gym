package cmd

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"

	"github.com/spf13/cobra"
	"gopkg.in/yaml.v3"
)

var testCmd = &cobra.Command{
	Use:   "test",
	Short: "Comando test que ejecuta el script de label en python",
	Run: func(cmd *cobra.Command, args []string) {

		yamlData, err := os.ReadFile("config.yaml")
		if err != nil {
			log.Fatalf("Error al leer config.yaml: %v", err)
		}

		var c Config
		if err := yaml.Unmarshal(yamlData, &c); err != nil {
			log.Fatalf("Error al parsear YAML: %v", err)
		}

		numImages, _ := cmd.Flags().GetInt("num")
		if numImages == 0 {
			numImages = c.Test.NumberOfImages
		}

		datasetPath := c.RawDataset.Path
		var outputPath string
		var saveImages string
		var showImages string

		if c.Test.SaveImages {
			outputPath = c.Test.OutputPath
			err = os.MkdirAll(outputPath, os.ModePerm)
			if err != nil {
				log.Fatal(err)
			}

		} else {
			outputPath = ""
		}

		if c.Test.SaveImages {
			saveImages = "True"
		} else {
			saveImages = "False"
		}

		if c.Test.ShowImages {
			showImages = "True"
		} else {
			showImages = "False"
		}

		comand := exec.Command("python/.venv/bin/python3", "python/main.py", "pretrain_test", datasetPath, fmt.Sprintf("%d", numImages), outputPath, saveImages, showImages)
		stdout, err := comand.StdoutPipe()
		if err != nil {
			log.Fatalln("Error executing comand")
		}

		if err := comand.Start(); err != nil {
			log.Fatalln("Error executing comand")
		}

		in := bufio.NewScanner(stdout)

		for in.Scan() {
			fmt.Print(in.Text())
		}

	},
}
