package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"net/http"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/gorilla/mux"
)

// ReqDeposit ...
type ReqDeposit struct {
	Amount  int     `json:"amount" validate:"required,min=10000,max=3000000"`
	Rate    float64 `json:"rate" validate:"required,min=1,max=8"`
	Date    string  `json:"date" validate:"required,datetime=02.01.2006"`
	Periods int     `json:"periods" validate:"required,min=1,max=60"`
}

// ResADeposit ...
type ResADeposit struct {
	Profit float64 `json:"profit"`
}

// ResError ...
type Error struct {
	Error string `json:"error"`
}

// API ..
type API struct {
	validate *validator.Validate
}

func main() {
	api := API{validate: validator.New()}

	r := mux.NewRouter()
	r.HandleFunc("/deposit", api.mdepositHandler).Methods(http.MethodPost)

	srv := &http.Server{
		Handler:      r,
		Addr:         ":8081",
		WriteTimeout: 10 * time.Second,
		ReadTimeout:  10 * time.Second,
	}

	fmt.Println(`Starting server at: "0.0.0.0:8081"`)
	log.Fatal(srv.ListenAndServe())
}

func (api *API) mdepositHandler(w http.ResponseWriter, r *http.Request) {
	var req ReqDeposit

	// Read json
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		abort(w, err, http.StatusBadRequest)
		return
	}

	// Validation
	if err := api.validate.Struct(req); err != nil {
		abort(w, err, http.StatusBadRequest)
		return
	}

	start, _ := time.Parse("02.01.2006", req.Date)

	response := make(map[string]float64, req.Periods)

	amount := float64(req.Amount)

	for i := 0; i <= req.Periods-1; i++ {
		amount = amount + amount*req.Rate/100/12
		dt := start.AddDate(0, i, 0)
		if start.Day() > dt.Day() {
			dt = dt.AddDate(0, 0, -3)
			dt = lastDayOfTheMonth(dt.Year(), dt.Month())
		}
		response[dt.Format("02.01.2006")] = math.Round(amount*100) / 100
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// abort ...
func abort(w http.ResponseWriter, err error, status int) {
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(Error{Error: err.Error()})
}

func lastDayOfTheMonth(year int, month time.Month) time.Time {
	if month++; month > 12 {
		month = time.Month(1)
		year++
	}
	t := time.Date(year, month, 0, 0, 0, 0, 0, time.UTC)
	return t
}
