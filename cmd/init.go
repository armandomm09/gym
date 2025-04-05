package cmd

import (
	"io"
	"log"
	"os"

	"github.com/spf13/cobra"
	"gopkg.in/yaml.v3"
)

var initCmd = &cobra.Command{

	Use:   "init",
	Short: "Init your workstation",
	Run: func(cmd *cobra.Command, args []string) {

		yaml_path := "config.yaml"

		yaml_path_flag, _ := cmd.Flags().GetString("path")
		if yaml_path_flag != "" {
			yaml_path = yaml_path_flag
		}
		config := Config{}

		config.Ontology = make(map[string]string)
		config.Ontology["a teal ball"] = "algae"
		config.Ontology["a white PVC tube"] = "coral"

		config.RawDataset.Path = "dataset"

		config.Test.InputPath = "dataset"
		config.Test.OutputPath = "runs/test"
		config.Test.NumberOfImages = 4
		config.Test.SaveImages = true
		config.Test.SaveImages = true

		config.GroundingDino.ModelPath = "models/grounding_dino.pth"
		config.GroundingDino.ConfidenceThreshold = 0.3
		config.GroundingDino.BoxThreshold = 0.25

		config.CLI.Mode = "pretrain_mode"
		config.CLI.Verbose = true

		config.Prueba = "prueba"
		// jsonn, _ := json.Marshal(config)

		yamlData, err := yaml.Marshal(&config)
		if err != nil {
			log.Fatal(err)
		}

		f, err := os.Create(yaml_path)
		if err != nil {
			log.Fatal(err)
		}

		defer f.Close()

		_, err = io.WriteString(f, string(yamlData))
		if err != nil {
			log.Fatal(err)
		}

		// print(string(jsonn))
	},
}
