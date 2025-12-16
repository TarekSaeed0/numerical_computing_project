import { Component, inject } from "@angular/core";
import {
  Router,
  RouterLink,
  RouterOutlet,
  NavigationEnd,
} from "@angular/router";
import { filter } from "rxjs";

@Component({
  selector: "app-root",
  imports: [RouterOutlet, RouterLink],
  templateUrl: "./app.component.html",
  styleUrl: "./app.component.css",
})
export class AppComponent {
  private router = inject(Router);

  tabs = [
    { label: "Equations Solver", path: "/equations-solver" },
    { label: "Root Finder", path: "/root-finder" },
    { label: "Integration", path: "/integration" },
  ];

  activeTabIndex = 0;

  ngOnInit(): void {
    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.activeTabIndex = this.tabs.findIndex(
          (tab) => tab.path === event.urlAfterRedirects,
        );
      });
  }
}
