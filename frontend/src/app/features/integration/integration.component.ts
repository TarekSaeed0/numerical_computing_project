import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  inject,
  signal,
  viewChild,
} from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { IntegrationService } from "./services/integration.service";
import { IntegrateRequest } from "./models/integrate-request";
import { functionValidator } from "../../shared/validators/function-validator";
import { IntegrateResponse } from "./models/integrate-response";
import { PlotComponent } from "./components/plot/plot.component";

@Component({
  selector: "app-integration",
  imports: [ReactiveFormsModule, AutoSizeInputDirective, PlotComponent],
  templateUrl: "./integration.component.html",
  styleUrl: "./integration.component.css",
})
export class IntegrationComponent {
  private integrationService = inject(IntegrationService);
  private formBuilder = inject(FormBuilder);
  private changeDetectorRef = inject(ChangeDetectorRef);

  readonly methods = [
    { label: "Trapezoid", value: "trapezoid" },
    { label: "Simpson's 1/3 Rule", value: "simpson-1-3" },
    { label: "Simpson's 3/8 Rule", value: "simpson-3-8" },
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
    lowerLimit: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
    upperLimit: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
    numberOfSubintervals: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    precision: ["", [Validators.pattern(/^[1-9]\d*$/)]],
  });

  function: string | null = null;
  lowerLimit: number | null = null;
  upperLimit: number | null = null;
  numberOfSubintervals: number | null = null;

  response = signal<IntegrateResponse | null>(null);

  resultElement = viewChild<ElementRef<HTMLDivElement>>("result");

  ngOnInit() {
    this.form.get("function")?.valueChanges.subscribe((f) => {
      if (this.form.get("function")?.valid) {
        this.function = f;
      }
    });

    this.form.get("lowerLimit")?.valueChanges.subscribe((lowerLimit) => {
      if (this.form.get("lowerLimit")?.valid) {
        this.lowerLimit = parseFloat(lowerLimit!);
      }
    });

    this.form.get("upperLimit")?.valueChanges.subscribe((upperLimit) => {
      if (this.form.get("upperLimit")?.valid) {
        this.upperLimit = parseFloat(upperLimit!);
      }
    });

    this.form.get("numberOfSubintervals")?.valueChanges.subscribe((n) => {
      if (this.form.get("numberOfSubintervals")?.valid) {
        this.numberOfSubintervals = isNaN(parseInt(n!, 10))
          ? 100
          : parseInt(n!, 10);
      }
    });
  }

  integrate() {
    // check if the form is valid, otherwise mark all fields as touched to show validation errors
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const value = this.form.value;

    // construct the request object, replacing empty strings with the default values
    const request: IntegrateRequest = {
      function: value.function!,
      method: value.method!,
      lowerLimit: value.lowerLimit!,
      upperLimit: value.upperLimit!,
      numberOfSubintervals: isNaN(parseInt(value.numberOfSubintervals!, 10))
        ? undefined
        : parseInt(value.numberOfSubintervals!, 10),
      precision: isNaN(parseInt(value.precision!, 10))
        ? undefined
        : parseInt(value.precision!, 10),
    };

    // send the request to the service
    this.integrationService.findRoot(request).subscribe((response) => {
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
