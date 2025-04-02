package tui_list_view

import (
	"fmt"
	"os"
	"test_viewer/cmd/utils"
	tui_expanded_elem "test_viewer/tui/expanded_elem"

	"github.com/charmbracelet/bubbles/key"
	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var (
	appStyle = lipgloss.NewStyle().Padding(1, 2)

	titleStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFFDF5")).
			Background(lipgloss.Color("#25A065")).
			Padding(0, 1)

	statusMessageStyle = lipgloss.NewStyle().
				Foreground(lipgloss.AdaptiveColor{Light: "#04B575", Dark: "#04B575"}).
				Render
)

type item struct {
	title       string
	avgTimes 	string
	totalTimes 	string
	data 		utils.Data
}

func (i item) Title() string       { return i.title }
func (i item) Description() string { return i.avgTimes }
func (i item) FilterValue() string { return i.title }

type listKeyMap struct {
	toggleStatusBar  key.Binding
	togglePagination key.Binding
	toggleHelpMenu   key.Binding
	selectItem 		 key.Binding
}

func newListKeyMap() *listKeyMap {
	return &listKeyMap{
		toggleStatusBar: key.NewBinding(
			key.WithKeys("S"),
			key.WithHelp("S", "toggle status"),
		),
		togglePagination: key.NewBinding(
			key.WithKeys("P"),
			key.WithHelp("P", "toggle pagination"),
		),
		toggleHelpMenu: key.NewBinding(
			key.WithKeys("H"),
			key.WithHelp("H", "toggle help"),
		),
		selectItem: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "Select test"),
		),
	}
}

type model struct {
	list list.Model
	keys *listKeyMap
	result utils.Result
	sub_model 		tea.Model
}

type itemDelegate struct {}

func newModel(result utils.Result) model {
	var (
		listKeys = newListKeyMap()
	)

	// Make initial list of items
	items := []list.Item{}
	for testName, test := range result.Data {
		items = append(items, item{testName, 
			fmt.Sprint("BIT avg: ",test.FenwickAvg, " Linear Avg: ", test.LinearAvg), 
			fmt.Sprint("BIT total: ",test.FenwickTotalTime, " Linear total: ", test.LinearTotalTime), test})
	}

	// Setup list
	list := list.New(items, list.NewDefaultDelegate(), 0, 0)
	list.Title = "Tests"
	list.Styles.Title = titleStyle
	list.AdditionalFullHelpKeys = func() []key.Binding {
		return []key.Binding{
			listKeys.toggleStatusBar,
			listKeys.togglePagination,
			listKeys.toggleHelpMenu,
		}
	}

	return model{
		list:          list,
		keys:          listKeys,
		result:  		result,
		sub_model:  	nil,
	}
}


func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	if m.sub_model != nil {
		var cmd tea.Cmd
		m.sub_model, cmd = m.sub_model.Update(msg)
		if sub_model_mod, ok := m.sub_model.(model); ok {
			m.list = sub_model_mod.list
			m.sub_model = nil
			return m, nil
		}
		return m, cmd
	}

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		h, v := appStyle.GetFrameSize()
		m.list.SetSize(msg.Width-h, msg.Height-v)

	case tea.KeyMsg:
		// Don't match any of the keys below if we're actively filtering.
		if m.list.FilterState() == list.Filtering {
			break
		}

		switch {
		case key.Matches(msg, m.keys.toggleStatusBar):
			m.list.SetShowStatusBar(!m.list.ShowStatusBar())
			return m, nil

		case key.Matches(msg, m.keys.togglePagination):
			m.list.SetShowPagination(!m.list.ShowPagination())
			return m, nil

		case key.Matches(msg, m.keys.toggleHelpMenu):
			m.list.SetShowHelp(!m.list.ShowHelp())
			return m, nil
		case key.Matches(msg, m.keys.selectItem):
			println("Selected item")
			item := m.list.SelectedItem().(item)
			m.sub_model = tui_expanded_elem.Entry(m.result, item.title)
			return m, nil
		}
	}

	// This will also call our delegate's update function.
	newListModel, cmd := m.list.Update(msg)
	m.list = newListModel
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}

func (m model) View() string {
	if m.sub_model != nil {
		return m.sub_model.View()
	}

	return appStyle.Render(m.list.View())
}

func Entry(result utils.Result) {

	if _, err := tea.NewProgram(newModel(result), tea.WithAltScreen()).Run(); err != nil {
		fmt.Println("Error running program:", err)
		os.Exit(1)
	}
}


