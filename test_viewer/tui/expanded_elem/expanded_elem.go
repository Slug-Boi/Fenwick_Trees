package tui_expanded_elem

import (
	"fmt"
	"sort"
	"strconv"
	"test_viewer/cmd/utils"

	"github.com/NimbleMarkets/ntcharts/barchart"
	"github.com/NimbleMarkets/ntcharts/canvas/runes"
	"github.com/charmbracelet/bubbles/table"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	zone "github.com/lrstanley/bubblezone"
)

var baseStyle = lipgloss.NewStyle().
	BorderStyle(lipgloss.NormalBorder()).
	BorderForeground(lipgloss.Color("63")) // purple

var blockStyle = lipgloss.NewStyle().
	Foreground(lipgloss.Color("9")). // red
	Background(lipgloss.Color("9"))  // red

var blockStyle2 = lipgloss.NewStyle().
	Foreground(lipgloss.Color("10")). // green
	Background(lipgloss.Color("10"))  // green

type model struct {
	table1       table.Model
	table2       table.Model
	selectedTest string
	testData     map[string]utils.TestData
	barChart     barchart.Model
	barData      []barchart.BarData
	zoneManager  *zone.Manager
}

func legend(bd barchart.BarData) (r string) {
	r = "Legend \n"
	for _, bv := range bd.Values {
		r += "\n" + bv.Style.Render(fmt.Sprintf("%c %s", runes.FullBlock, bv.Name))
	}
	return
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "esc":
			if m.table1.Focused() {
				m.table1.Blur()
				m.table2.Focus()
			} else if m.table2.Focused() {
				m.table2.Blur()
			} else {
				m.table1.Focus()
			}
		case "q", "ctrl+c":
			return m, tea.Quit
		case "enter":
			if m.table2.Focused() {
				m.selectedTest = m.table2.SelectedRow()[0]
				m.updateBarChart()
				return m, nil
			}
		}
	}

	if m.table1.Focused() {
		m.table1, cmd = m.table1.Update(msg)
	} else if m.table2.Focused() {
		m.table2, cmd = m.table2.Update(msg)
	}
	return m, cmd
}

const minVisibleHeight = 0.1

var max_value = 0.0

func (m *model) updateBarChart() {
	// Clear existing data
	m.barChart.Clear()

	// Sort test keys numerically
	testKeys := make([]string, 0, len(m.testData))
	for k := range m.testData {
		testKeys = append(testKeys, k)
	}
	sort.Slice(testKeys, func(i, j int) bool {
		numI, _ := strconv.Atoi(testKeys[i])
		numJ, _ := strconv.Atoi(testKeys[j])
		return numI < numJ
	})

	// Add data to bar chart
	values := []barchart.BarData{}
	for _, testKey := range testKeys {
		test := m.testData[testKey]

		// Ensure zero values have minimum visible height
		fenwickValue, _ := strconv.ParseFloat(fmt.Sprintf("%.2f", test.FenwickTime), 64)
		linearValue, _ := strconv.ParseFloat(fmt.Sprintf("%.2f", test.LinearTime), 64)

		if linearValue > max_value {
			max_value = linearValue
		}
		if fenwickValue > max_value {
			max_value = fenwickValue
		}

		// Add both linear and Fenwick times for each test
		values = append(values, barchart.BarData{
			Label: fmt.Sprint("test ", testKey),
			Values: []barchart.BarValue{
				{Name: "linear", Value: linearValue, Style: blockStyle},
				{Name: "BIT", Value: fenwickValue, Style: blockStyle2},
			},
		})

	}

	m.barData = values
	m.barChart.PushAll(values)
	m.barChart.Draw()
}

func (m model) View() string {
	// Render tables side by side
	tables := lipgloss.JoinHorizontal(
		lipgloss.Top,
		baseStyle.Render(m.table1.View()),
		lipgloss.NewStyle().Width(2).Render(""),
		baseStyle.Render(m.table2.View()),
	)

	// Render bar chart with title
	chartView := lipgloss.JoinVertical(
		lipgloss.Left,
		lipgloss.NewStyle().
			Bold(true).
			PaddingBottom(1).
			Render("Performance Comparison (ms)"),
		baseStyle.Render(m.barChart.View()),
	)

	chartLengend := lipgloss.JoinVertical(
		lipgloss.Left,
		lipgloss.NewStyle().
			Bold(true).
			PaddingBottom(1).Render(""),
		baseStyle.Render(legend(m.barData[0])))

	// Combine tables and chart
	fullView := lipgloss.JoinHorizontal(
		lipgloss.Top,
		tables,
		lipgloss.NewStyle().Width(4).Render(""),
		chartView,
		lipgloss.NewStyle().Width(2).Render(""),
		chartLengend,
	)

	return fullView + "\n"
}

func Entry(result utils.Result, test_name string) tea.Model {
	// First table (timing info)
	columns1 := []table.Column{
		{Title: "", Width: 30},
		{Title: "Value", Width: 20},
	}

	rows1 := []table.Row{
		{"Linear Avg Time: ", fmt.Sprintf("%f", result.Data[test_name].LinearAvg)},
		{"Fenwick Avg Time: ", fmt.Sprintf("%f", result.Data[test_name].FenwickAvg)},
		{"Linear Total Time: ", fmt.Sprintf("%f", result.Data[test_name].LinearTotalTime)},
		{"Fenwick Total Time: ", fmt.Sprintf("%f", result.Data[test_name].FenwickTotalTime)},
	}

	// Second table (test info)
	columns2 := []table.Column{
		{Title: "Test", Width: 10},
		{Title: "Position", Width: 20},
		{Title: "Linear", Width: 10},
		{Title: "Fenwick", Width: 10},
	}

	var rows2 []table.Row
	for testNum, testData := range result.Data[test_name].Tests {
		rows2 = append(rows2, table.Row{
			testNum,
			fmt.Sprintf("%v", testData.QueryPosition),
			fmt.Sprintf("%f", testData.LinearTime),
			fmt.Sprintf("%f", testData.FenwickTime),
		})
	}

	// Create tables
	t1 := table.New(
		table.WithColumns(columns1),
		table.WithRows(rows1),
		table.WithFocused(true),
		table.WithHeight(7),
	)

	t2 := table.New(
		table.WithColumns(columns2),
		table.WithRows(rows2),
		table.WithFocused(false),
		table.WithHeight(7),
	)

	// Apply table styles
	s := table.DefaultStyles()
	s.Header = s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		BorderBottom(true).
		Bold(false)
	s.Selected = s.Selected.
		Foreground(lipgloss.Color("229")).
		Background(lipgloss.Color("57")).
		Bold(false)
	t1.SetStyles(s)
	t2.SetStyles(s)

	zoneManager := zone.New()

	// Create bar chart (width, height, max value)
	//TODO: Change 25 to be based on max value later
	barChart := barchart.New(40, 25, barchart.WithZoneManager(zoneManager))
	// barChart.SetShowXLabel(true)
	// barChart.SetXLabel("Test Number")

	// Create model
	m := model{
		table1:      t1,
		table2:      t2,
		barChart:    barChart,
		testData:    result.Data[test_name].Tests,
		zoneManager: zoneManager,
	}

	m.barChart.Draw()

	// Update chart with initial data
	m.updateBarChart()

	// Start program
	return m
}
