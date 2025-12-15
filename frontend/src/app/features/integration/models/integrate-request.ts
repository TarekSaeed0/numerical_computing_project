export type IntegrateRequest = {
  function: string;
  method: "trapezoid" | "simpson-1-3" | "simpson-3-8";
  lowerLimit: string;
  upperLimit: string;
  numberOfSubintervals: number;
  precision?: number;
};
