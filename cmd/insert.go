package cmd

import (
	"fmt"
	"log"

	"github.com/spf13/cobra"
)

var insertVideoCmd = &cobra.Command{

	Use:   "insertv",
	Short: "Insert frames from video into raw dataset",
	Run: func(cmd *cobra.Command, args []string) {

		video_path, _ := cmd.Flags().GetString("path")
		if video_path == "" {
			log.Fatal("No video path provided")
		}

		frames_count, _ := cmd.Flags().GetInt("frames")
		if frames_count == 0 {
			frames_count = 30
		}

		c := getConfig()

		raw_dataset_path := c.RawDataset.Path

		execute_python_script("python/main.py", "insert_video_in_raw", video_path, fmt.Sprintf("%v", frames_count), raw_dataset_path)

	},
}
