use actix_web::http::StatusCode;
use actix_web::{web, App, HttpResponse, HttpServer, ResponseError};
use chrono::{Datelike, NaiveDate};
use serde::{Deserialize, Serialize};
use serde_json::{json, to_string_pretty};
use std::collections::HashMap;
use std::fmt::{Display, Formatter, Result as FmtResult};
use std::io;
use validator::{Validate, ValidationError};

#[derive(Debug, Deserialize, Serialize, Validate)]
struct Request {
    #[validate(range(min = 1, max = 8, message = "Bad rate"))]
    rate: f64,
    #[validate(range(min = 10000, max = 3000000, message = "Bad amount"))]
    amount: f64,
    #[validate(range(min = 1, max = 60, message = "Bad period"))]
    periods: i32,
    #[validate(length(equal = 10), custom = "validate_udate")]
    date: String,
}

#[derive(Debug, Serialize)]
struct Error {
    msg: String,
    status: u16,
}

async fn mdeposit(payload: web::Json<Request>) -> Result<HttpResponse, Error> {
    let mut response = HashMap::new();

    if let Err(e) = payload.validate() {
        return Err(Error {
            msg: format!("{}", e),
            status: 400,
        });
    };

    let mut amount = payload.amount;
    let dt = NaiveDate::parse_from_str(&payload.date, "%d.%m.%Y").unwrap();
    let mut y = dt.year();
    let mut m = dt.month();
    let f_day = dt.day();
    let mut d = f_day;

    for _ in 0..payload.periods {
        amount += amount * payload.rate / 100.0 / 12.0;

        let date = format!("{day:#02}.{month:#02}.{year}", day = d, month = m, year = y);
        response.insert(date, f64::trunc(amount * 100.0) / 100.0);

        if m == 12 {
            y += 1;
            m = 1;
        } else {
            m += 1;
        }
        let l_day = last_day_of_month(y, m);
        if f_day >= l_day {
            d = l_day;
        }
    }

    Ok(HttpResponse::Ok()
        .content_type("application/json")
        .body(serde_json::to_string(&response).unwrap()))
}

fn last_day_of_month(year: i32, month: u32) -> u32 {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => {
            if is_leap_year(year) {
                29
            } else {
                28
            }
        }
        _ => panic!("invalid month: {}", month),
    }
}

fn is_leap_year(year: i32) -> bool {
    return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
}

impl Display for Error {
    fn fmt(&self, f: &mut Formatter) -> FmtResult {
        write!(f, "{}", to_string_pretty(self).unwrap())
    }
}

impl ResponseError for Error {
    fn error_response(&self) -> web::HttpResponse {
        let err_json = json!({ "error": self.msg });
        web::HttpResponse::build(StatusCode::from_u16(self.status).unwrap()).json(err_json)
    }
}

fn validate_udate(date: &str) -> Result<(), ValidationError> {
    if let Err(_) = NaiveDate::parse_from_str(date, "%d.%m.%Y") {
        return Err(ValidationError::new("bad date"));
    }
    Ok(())
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    let endpoint = "0.0.0.0:8080";

    println!("Starting server at: {:?}", endpoint);
    HttpServer::new(|| {
        App::new().service(web::resource("/deposit").route(web::post().to(mdeposit)))
    })
    .bind(endpoint)?
    .run()
    .await
}
