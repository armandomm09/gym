package cmd

// Config es el struct principal que mapea todo el YAML.
type Config struct {
	Ontology      map[string]string   `yaml:"ontology"`
	RawDataset    RawDatasetConfig    `yaml:"raw_dataset"`
	Dataset       DatasetConfig       `yaml:"dataset"`
	Test          TestConfig          `yaml:"test"`
	GroundingDino GroundingDinoConfig `yaml:"grounding_dino"`
	CLI           CLIConfig           `yaml:"cli"`
	Prueba        string              `yaml:"prueba"`
}

type DatasetConfig struct {
	Path string `yaml:"path"`
}

// RawDatasetConfig representa la sección "dataset".
type RawDatasetConfig struct {
	Path string `yaml:"path"`
}

// TestConfig representa la sección "test".
type TestConfig struct {
	InputPath      string `yaml:"input_path"`
	OutputPath     string `yaml:"output_path"`
	NumberOfImages int    `yaml:"number_of_images"`
	ShowImages     bool   `yaml:"show"`
	SaveImages     bool   `yaml:"save"`
}

// GroundingDinoConfig representa la sección "grounding_dino".
type GroundingDinoConfig struct {
	ModelPath           string  `yaml:"model_path"`
	ConfidenceThreshold float64 `yaml:"confidence_threshold"`
	BoxThreshold        float64 `yaml:"box_threshold"`
}

// CLIConfig representa la sección "cli".
type CLIConfig struct {
	Mode    string `yaml:"mode"`
	Verbose bool   `yaml:"verbose"`
}
