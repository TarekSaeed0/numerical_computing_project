import { Component, input, OnChanges, SimpleChanges } from "@angular/core";
import { all, create, EvalFunction } from "mathjs";
import { PlotlyComponent } from "angular-plotly.js";
import { PlotRelayoutEvent } from "plotly.js-dist-min";

const math = create(all, { predictable: true });

@Component({
  selector: "app-plot",
  imports: [PlotlyComponent],
  templateUrl: "./plot.component.html",
  styleUrl: "./plot.component.css",
})
export class PlotComponent implements OnChanges {
  function = input<string | null>(null);
  lowerLimit = input<number | null>(null);
  upperLimit = input<number | null>(null);
  compiledFunction: EvalFunction | null = null;

  minX = -10;
  maxX = 10;

  numberOfPoints = 1000;

  data: any[] = [];

  layout = {
    dragmode: "pan",
    margin: { l: 30, r: 30, t: 30, b: 30 },
    xaxis: { range: [this.minX, this.maxX], exponentformat: "power" },
    yaxis: { range: [this.minX, this.maxX], exponentformat: "power" },
    width: 400,
    height: 350,
    colorway: ["#2b7fff", "#fb2c36", "#00c951", "#efb100"],
    showlegend: false,
  };

  config = {
    displaylogo: false,
    modeBarButtonsToRemove: ["toImage"],
  };

  ngOnChanges(changes: SimpleChanges): void {
    if (changes["function"]) {
      this.compileFunction();
      this.generateData();
    }
    if (
      (changes["lowerLimit"] || changes["upperLimit"]) &&
      this.lowerLimit() !== null &&
      this.upperLimit() !== null
    ) {
      console.log("Test1");
      this.generateData();
    }
  }

  compileFunction() {
    const f = this.function();
    if (f) {
      this.compiledFunction = math.compile(f);
    }
  }

  generateData() {
    const step = (this.maxX - this.minX) / (this.numberOfPoints - 1);
    const x = Array.from(
      { length: this.numberOfPoints },
      (_, i) => this.minX + i * step,
    );
    const y = x.map((x) => this.compiledFunction?.evaluate({ x }));
    this.data = [
      {
        x,
        y,
        type: "scatter",
        mode: "lines",
        name: "f(x)",
      },
    ];

    if (this.lowerLimit()!== null && this.upperLimit()!== null) {
      this.data = [
        ...this.data,
        {
          x: x.filter(
            (x) => x >= this.lowerLimit()! && x <= this.upperLimit()!,
          ),
          y: y.filter(
            (_, i) => x[i] >= this.lowerLimit()! && x[i] <= this.upperLimit()!,
          ),
          fill: "tozeroy",
          type: "scatter",
          mode: "lines",
          name: "Integration Area",
          fillcolor: "rgba(0, 0, 255, 0.2)",
          line: { color: "transparent" },
        },
      ];
    }
  }

  onRelayout(event: PlotRelayoutEvent) {
    if (
      event["xaxis.range[0]"] !== undefined &&
      event["xaxis.range[1]"] !== undefined
    ) {
      this.minX = event["xaxis.range[0]"] as number;
      this.maxX = event["xaxis.range[1]"] as number;
      this.generateData();
    }
  }
}
