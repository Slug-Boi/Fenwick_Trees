package utils

import (
	"encoding/json"
	"os"
)

type TestData struct {
	QueryPosition []int   `json:"query_position"`
	LinearTime    float64 `json:"linear_time"`
	LinearResult  int     `json:"linear_result"`
	FenwickTime   float64 `json:"fenwick_time"`
	FenwickResult int     `json:"fenwick_result"`
}

type Data struct {
	Dimension        []int               `json:"dimension"`
	NumTests         int                 `json:"num_tests"`
	MaxValue         float64             `json:"max_value"`
	RandomRange      []int               `json:"random_range"`
	Tests            map[string]TestData `json:"tests"`
	LinearAvg        float64             `json:"linear_avg"`
	FenwickAvg       float64             `json:"fenwick_avg"`
	LinearTotalTime  float64             `json:"linear_total_time"`
	FenwickTotalTime float64             `json:"fenwick_total_time"`
}

type Result struct {
	Data map[string]Data `json:"-"`
}

// UnmarshalJSON implements custom unmarshaler to handle dynamic keys like "rand 0", "rand 1"
func (r *Result) UnmarshalJSON(data []byte) error {
	r.Data = make(map[string]Data)
	var temp map[string]json.RawMessage
	if err := json.Unmarshal(data, &temp); err != nil {
		return err
	}

	for key, value := range temp {
		var rd Data
		if err := json.Unmarshal(value, &rd); err != nil {
			return err
		}
		r.Data[key] = rd
	}
	return nil
}

func readJSON(jsonDataPath string) []byte {
	jsonData, err := os.ReadFile(jsonDataPath)
	if err != nil {
		panic(err)
	}
	return jsonData
}

func ParseJSON(jsonDataPath string) Result {
	// Read the json file
	jsonData := readJSON(jsonDataPath)

	var result Result
	err := json.Unmarshal(jsonData, &result)
	if err != nil {
		panic(err)
	}

	return result
}
