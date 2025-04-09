package cmd

import (
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/spf13/cobra"
)

var openLabelerCmd = &cobra.Command{

	Use:   "label",
	Short: "Opens label studio to start labeling",
	Run: func(cmd *cobra.Command, args []string) {

		c := getConfig()

		key := c.LabelStudio.Key
		url := c.LabelStudio.Url
		title := strings.ReplaceAll(c.Project.Title, " ", "_")

		fmt.Println("EXECUTING")
		killLabelStudio()
		command := exec.Command("zsh", "-c", "source python/.venv/bin/activate && label-studio")
		go command.Run()
		time.Sleep(7 * time.Second)

		execute_python_script("-u", "python/main.py", "label", key, url, title)

	},
}
