"use client";
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
import Paginated from "../components/pagination";
import { ScheduleTable } from "../components/schedule";

interface Event {
  name: "string",
  start_time: "string",
  venue: "string"
}

export default function Schedule({ params }: { params: { daynum: string } }) {
  const { daynum } = params;
  const [count, setCount] = React.useState(0);
  const [events, setEvents] = React.useState<Event[]>([]);

  return (
    <main className="flex flex-col items-center justify-center h-screen">
      <ScheduleTable day={daynum} events={events} setEvents={setEvents} setCount={setCount} />
      <Paginated daynum={daynum} count={count} />
    </main>
  );
}
