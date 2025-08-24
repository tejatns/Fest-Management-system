"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";
import { Icons } from "@/components/icons";

export function MainNav() {
  const pathname = usePathname();

  return (
    <div className="mr-4 hidden md:flex">
      <Link href="/" className="mr-6 flex items-center space-x-2">
        <Icons.logo className="h-6 w-6" />
      </Link>
      <nav className="flex items-center gap-6 text-sm">
        <Link
          href="/"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname === "/" ? "text-foreground" : "text-foreground/60"
          )}
        >
          <span className="sr-only">Home</span>
          Home
        </Link>
        <Link
          href="/schedule"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname?.startsWith("/schedule")
              ? "text-foreground"
              : "text-foreground/60"
          )}
        >
          <span className="sr-only">Schedule</span>
          Schedule
        </Link>
        <Link
          href="/events"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname?.startsWith("/events")
              ? "text-foreground"
              : "text-foreground/60"
          )}
        >
          <span className="sr-only">Events</span>
          Events
        </Link>
        {/* <Link
          href="/examples"
          className={cn(
            "transition-colors hover:text-foreground/80",
            pathname?.startsWith("/examples")
              ? "text-foreground"
              : "text-foreground/60"
          )}
        >
          Examples
        </Link> */}
      </nav>
    </div>
  );
}
