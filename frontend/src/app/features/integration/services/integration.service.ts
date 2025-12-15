import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { Observable, catchError, of, map } from "rxjs";
import { IntegrateRequest } from "../models/integrate-request";
import { IntegrateResponse } from "../models/integrate-response";

@Injectable({
  providedIn: "root",
})
export class IntegrationService {
  private http = inject(HttpClient);
  private readonly baseUrl = "http://localhost:5000/api";

  // maps the IntegrateRequest to the format expected by the backend API.
  private mapRequest(request: IntegrateRequest) {
    return {
      function: request.function,
      method: request.method,
      lower_limit: request.lowerLimit,
      upper_limit: request.upperLimit,
      number_of_subintervals: request.numberOfSubintervals,
      precision: request.precision,
    };
  }

  // maps the backend API response to the IntegrateResponse format.
  private mapResponse(response: any): IntegrateResponse {
    return {
      value: response.value,
      absoluteError: response.absolute_error,
      executionTime: response.execution_time,
      message: response.message,
    };
  }

  findRoot(request: IntegrateRequest): Observable<IntegrateResponse> {
    return this.http
      .post<{
        value?: string;
        absolute_error?: string;
        execution_time?: number;
        message: string;
      }>(`${this.baseUrl}/integrate`, this.mapRequest(request))
      .pipe(
        catchError((error) =>
          of({
            message: error.error.error,
          }),
        ),
        map((response) => this.mapResponse(response)),
      );
  }
}
