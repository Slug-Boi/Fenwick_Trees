/*
Copyright © 2025 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"os"
	"test_viewer/cmd/utils"
	"test_viewer/tui/file_picker"
	tui_list_view "test_viewer/tui/list_view"

	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "test_viewer",
	Short: "A small tui application for reading json data and displaying it in a list format with graphs",
	Long: `A small tui application for reading json data and displaying it in a list format with graphs`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	Run: func(cmd *cobra.Command, args []string) {
		var path string

		if len(args) == 0 {
			// Start filepicker
			path = tui_filepicker.Entry()

		} else {
			path = args[0]
		}

		// Read the json file
		result := utils.ParseJSON(path)

		tui_list_view.Entry(result)

	 },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}


