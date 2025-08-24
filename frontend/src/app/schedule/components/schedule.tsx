import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import React, { useEffect } from "react";

interface Event {
  name: "string";
  start_time: "string";
  venue: "string";
}

export function ScheduleTable({
  day,
  events,
  setEvents,
  setCount,
}: {
  day: string;
  events: Event[];
  setEvents: (events: Event[]) => void;
  setCount: (count: number) => void;
}) {
  const [date, setDate] = React.useState("");
  useEffect(() => {
    dateFetch();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (date !== "") eventFetch();
  }, [date]); // eslint-disable-line react-hooks/exhaustive-deps

  function dateFetch() {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/schedule/dates`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setDate(data[parseInt(day) - 1]);
        setCount(data.length);
      })
      .catch((err) => console.log(err));
  }

  function eventFetch() {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/schedule/${date}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setEvents(data))
      .catch((err) => console.log(err));
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Events</CardTitle>
        <CardDescription>{date}</CardDescription>
      </CardHeader>
      <CardContent>
        <Table className="w-full">
          <TableCaption>List of Events</TableCaption>
          <TableHeader>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Venue</TableCell>
              <TableCell>Start Time</TableCell>
            </TableRow>
          </TableHeader>
          <TableBody>
            {events?.map((event) => (
              <TableRow key={event.name}>
                <TableCell className="font-medium">{event.name}</TableCell>
                <TableCell>{event.venue}</TableCell>
                <TableCell className="text-right">{event.start_time}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
