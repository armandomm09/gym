package cmd

type Config struct {
	Project       ProjectS            `yaml:"project"`
	LabelStudio   LabelStudioConfig   `yaml:"ls"`
	Ontology      map[string]string   `yaml:"ontology"`
	RawDataset    RawDatasetConfig    `yaml:"raw_dataset"`
	Dataset       DatasetConfig       `yaml:"dataset"`
	Test          TestConfig          `yaml:"test"`
	GroundingDino GroundingDinoConfig `yaml:"grounding_dino"`
	CLI           CLIConfig           `yaml:"cli"`
	Prueba        string              `yaml:"prueba"`
}

type ProjectS struct {
	Title string `yaml:"title"`
}

type LabelStudioConfig struct {
	Key string `yaml:"key"`
	Url string `yaml:"url"`
}
type DatasetConfig struct {
	Path string `yaml:"path"`
}

type RawDatasetConfig struct {
	Path string `yaml:"path"`
}

type TestConfig struct {
	InputPath      string `yaml:"input_path"`
	OutputPath     string `yaml:"output_path"`
	NumberOfImages int    `yaml:"number_of_images"`
	ShowImages     bool   `yaml:"show"`
	SaveImages     bool   `yaml:"save"`
}

type GroundingDinoConfig struct {
	ModelPath           string  `yaml:"model_path"`
	ConfidenceThreshold float64 `yaml:"confidence_threshold"`
	BoxThreshold        float64 `yaml:"box_threshold"`
}

type CLIConfig struct {
	Mode    string `yaml:"mode"`
	Verbose bool   `yaml:"verbose"`
}
