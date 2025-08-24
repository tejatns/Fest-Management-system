"use client";

export interface Event {
  id: string;
  name: string;
  date: string;
  venue: string;
  type: string;
  desc: string;
}

import * as React from "react";
import Autoplay from "embla-carousel-autoplay";

import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import dynamic from "next/dynamic";
import DrawerDialogDemo from "./wrapper";

export default function CarouselPlugin() {
  const plugin = React.useRef(
    Autoplay({ delay: 2000, stopOnInteraction: true })
  );

  const [EventList, setEventList] = React.useState<Event[]>([]);
  const [UserRole, setUserRole] = React.useState<string>("");

  React.useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/events/all`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setEventList(data.events);
      });
  }, []);

  React.useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/role`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setUserRole(data.role);
      });
  }, []);

  return (
    <main className="flex items-center justify-center h-screen">
      <Carousel
        plugins={[plugin.current]}
        className="w-full max-w-sm"
        onMouseEnter={plugin.current.stop}
        onMouseLeave={plugin.current.reset}
      >
        <CarouselContent>
          {EventList.map((event, index) => (
            <CarouselItem key={index} className="ring ring-400 ring-opacity-50">
              {/* <div className="p-1"> */}
              {/* <Card className="w-full h-full"> */}
              <DrawerDialogDemo event={event} UserRole={UserRole} />
              {/* </Card> */}
              {/* </div> */}
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </main>
  );
}
