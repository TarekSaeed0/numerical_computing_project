import { Routes } from "@angular/router";
import { EquationsSolverComponent } from "./features/equations-solver/equations-solver.component";
import { RootFinderComponent } from "./features/root-finder/root-finder.component";
import { IntegrationComponent } from "./features/integration/integration.component";

export const routes: Routes = [
  { path: "", redirectTo: "/equations-solver", pathMatch: "full" },
  {
    path: "equations-solver",
    component: EquationsSolverComponent,
    title: "System of Linear Equations Solver",
    data: { order: 0 },
  },
  {
    path: "root-finder",
    component: RootFinderComponent,
    title: "Root Finder",
    data: { order: 1 },
  },
  {
    path: "integration",
    component: IntegrationComponent,
    title: "Integration",
    data: { order: 2 },
  },
];
