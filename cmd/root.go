package cmd

import (
	"fmt"
	"log"
	"os"

	"github.com/spf13/cobra"
	"gopkg.in/yaml.v3"
)

var rootCmd = &cobra.Command{
	Use:   "app",
	Short: "Comando raíz que imprime HELLOOO o la configuración",
	Run: func(cmd *cobra.Command, args []string) {

		configKey, _ := cmd.Flags().GetString("config")

		if cmd.Flags().Changed("config") {

			yamlData, err := os.ReadFile("config.yaml")
			if err != nil {
				log.Fatalf("Error al leer config.yaml: %v", err)
			}

			var c Config
			if err := yaml.Unmarshal(yamlData, &c); err != nil {
				log.Fatalf("Error al parsear YAML: %v", err)
			}

			switch configKey {
			case "ontology":
				out, err := yaml.Marshal(c.Ontology)
				if err != nil {
					log.Fatalf("Error al serializar ontology: %v", err)
				}
				fmt.Print(string(out))
			case "dataset":
				out, err := yaml.Marshal(c.RawDataset)
				if err != nil {
					log.Fatalf("Error al serializar dataset: %v", err)
				}
				fmt.Print(string(out))
			case "grounding_dino":
				out, err := yaml.Marshal(c.GroundingDino)
				if err != nil {
					log.Fatalf("Error al serializar grounding_dino: %v", err)
				}
				fmt.Print(string(out))
			case "cli":
				out, err := yaml.Marshal(c.CLI)
				if err != nil {
					log.Fatalf("Error al serializar cli: %v", err)
				}
				fmt.Print(string(out))
			case "test":
				out, err := yaml.Marshal(c.Test)
				if err != nil {
					log.Fatalf("Error al serializar cli: %v", err)
				}
				fmt.Print(string(out))
			case "prueba":
				fmt.Println(c.Prueba)
			case "all":
				fallthrough
			default:
				out, err := yaml.Marshal(c)
				if err != nil {
					log.Fatalf("Error al serializar config completo: %v", err)
				}
				fmt.Print(string(out))
			}
			return
		}

		fmt.Println("HELLOOO")
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().StringP("config", "c", "", "Muestra la configuración completa o una sección específica (por ejemplo, 'ontology')")
	rootCmd.Flags().Lookup("config").NoOptDefVal = "all"

	rootCmd.AddCommand(testCmd)
	testCmd.Flags().IntP("num", "n", 0, "Número de imágenes para el test (por defecto se toma del archivo de configuración)")

	rootCmd.AddCommand(initCmd)
	initCmd.Flags().StringP("path", "p", "", "Definir el path del config.yaml")

	rootCmd.AddCommand(insertVideoCmd)
	insertVideoCmd.Flags().StringP("path", "p", "", "The path of the video to add to the raw dataset")
	insertVideoCmd.Flags().IntP("frames", "f", 0, "The number of between how many frames, a frame will be added to the video")

	rootCmd.AddCommand(autolabelCmd)

	rootCmd.AddCommand(openLabelerCmd)
}
