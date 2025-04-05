package cmd

import (
	"encoding/json"
	"log"

	"github.com/spf13/cobra"
)

var autolabelCmd = &cobra.Command{

	Use:   "autolabel",
	Short: "Start autolabeling work",
	Run: func(cmd *cobra.Command, args []string) {
		c := getConfig()

		ontology, err := json.Marshal(c.Ontology)
		if err != nil {
			log.Fatal(err)
		}
		inputFolder := c.RawDataset.Path
		outputFolder := c.Dataset.Path
		execute_python_script("python/main.py", "autolabel", string(ontology), inputFolder, outputFolder)
		// print(string(jsonn))
	},
}
