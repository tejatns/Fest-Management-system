"use client";
// Path: src/app/schedule/[[day]].tsx
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Timeline, TimelineItem } from "@/components/ui/timeline";
import * as React from "react";
import { set } from "zod";
import Paginated from "./components/pagination";
import { ScheduleTable } from "./components/schedule";

interface Event {
  name: "string",
  start_time: "string",
  venue: "string"
}


export default function Schedule() {
  const daynum = "1";
  const [count, setCount] = React.useState(0);
  const [events, setEvents] = React.useState<Event[]>([]);

  React.useEffect(() => {
    if (!localStorage.getItem("token")) {
      window.location.href = "/auth";
    }
  }, []);

  return (
    <main className="flex flex-col items-center justify-center h-screen">
      <ScheduleTable day={daynum} events={events} setEvents={setEvents} setCount={setCount} />
      <Paginated daynum={daynum} count={count} />
    </main>
  );
}
