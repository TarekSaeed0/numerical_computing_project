import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  inject,
  signal,
  viewChild,
} from "@angular/core";
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators,
  AbstractControl,
  ValidationErrors,
} from "@angular/forms";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { FunctionNode, OperatorNode, parse, SymbolNode } from "mathjs";
import { PlotComponent } from "./components/plot/plot.component";
import { ParametersComponent } from "./components/parameters/parameters.component";
import { FindRootResponse } from "./models/find-root-response";
import { IntervalParametersComponent } from "./components/parameters/interval-parameters/interval-parameters.component";
import { OneGuessParametersComponent } from "./components/parameters/one-guess-parameters/one-guess-parameters.component";
import { TwoGuessesParametersComponent } from "./components/parameters/two-guesses-parameters/two-guesses-parameters.component";
import { OneGuessWithMultiplicityParametersComponent } from "./components/parameters/one-guess-with-multiplicity-parameters/one-guess-with-multiplicity-parameters.component";
import { FindRootRequest } from "./models/find-root-request";
import { RootFinderService } from "./services/root-finder.service";
import { functionValidator } from "../../shared/validators/function-validator";

@Component({
  selector: "app-root-finder",
  imports: [
    ReactiveFormsModule,
    AutoSizeInputDirective,
    PlotComponent,
    IntervalParametersComponent,
    OneGuessParametersComponent,
    OneGuessWithMultiplicityParametersComponent,
    TwoGuessesParametersComponent,
  ],
  templateUrl: "./root-finder.component.html",
  styleUrl: "./root-finder.component.css",
})
export class RootFinderComponent {
  private rootFinderService = inject(RootFinderService);
  private formBuilder = inject(FormBuilder);
  private changeDetectorRef = inject(ChangeDetectorRef);

  readonly methods = [
    { label: "Bisection", value: "bisection" },
    { label: "False-Position", value: "false-position" },
    { label: "Fixed-Point", value: "fixed-point" },
    { label: "Newton-Raphson", value: "newton-raphson" },
    { label: "Modified Newton-Raphson", value: "modified-newton-raphson" },
    { label: "Secant", value: "secant" },
  ] as const;

  methodLabels = Object.fromEntries(
    this.methods.map(({ label, value }) => [value, label] as const),
  );

  form = this.formBuilder.group({
    function: ["", [Validators.required, functionValidator]],
    method: [
      this.methods[0].value as (typeof this.methods)[number]["value"],
      Validators.required,
    ],
    precision: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    numberOfIterations: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    absoluteRelativeError: ["", [Validators.pattern(/^[-+]?\d+(\.\d+)?$/)]],
    parameters: [null as any],
  });

  functions: { [k: string]: string } = {};

  parameters = viewChild<ParametersComponent>("parameters");
  parametersElement = viewChild("parameters", { read: ElementRef });

  response = signal<FindRootResponse | null>(null);

  resultElement = viewChild<ElementRef<HTMLDivElement>>("result");

  ngOnInit() {
    this.form.get("function")?.valueChanges.subscribe((f) => {
      if (this.form.get("function")?.valid) {
        if (this.form.get("method")?.value === "fixed-point") {
          this.functions = { ["g(x)"]: f!, ["x"]: "x" };
        } else {
          this.functions = { ["f(x)"]: f! };
        }
      }
    });

    this.form.get("method")?.valueChanges.subscribe((method) => {
      if (
        this.form.get("function")?.valid ||
        this.functions["f(x)"] ||
        this.functions["g(x)"]
      ) {
        if (method === "fixed-point") {
          this.functions = {
            ["g(x)"]: this.functions["f(x)"],
            ["x"]: "x",
          };
        } else if (this.functions["g(x)"]) {
          this.functions = {
            ["f(x)"]: this.functions["g(x)"],
          };
        }
      }

      this.form.setControl("parameters", this.formBuilder.control(null));
      this.changeDetectorRef.detectChanges();
      // scroll to show the parameters section
      setTimeout(() => {
        this.parametersElement()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
  }

  solve() {
    // check if the form is valid, otherwise mark all fields as touched to show validation errors
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.parameters()?.form.markAllAsTouched();
      return;
    }

    const value = this.form.value;

    // construct the request object, replacing empty strings with the default values
    const request: FindRootRequest = {
      function: value.function!,
      method: value.method!,
      numberOfIterations: isNaN(parseInt(value.numberOfIterations!, 10))
        ? undefined
        : parseInt(value.numberOfIterations!, 10),
      absoluteRelativeError:
        value.absoluteRelativeError!.trim() === ""
          ? undefined
          : value.absoluteRelativeError!,
      precision: isNaN(parseInt(value.precision!, 10))
        ? undefined
        : parseInt(value.precision!, 10),
      parameters: this.parameters()?.parameters as any,
    };

    // send the request to the service
    this.rootFinderService.findRoot(request).subscribe((response) => {
      // hide steps and show the result
      this.response.set(response);
      this.changeDetectorRef.detectChanges();
      // scroll to show the result
      setTimeout(() => {
        this.resultElement()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
  }
}
