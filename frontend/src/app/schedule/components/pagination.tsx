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
import * as React from "react";

export default function Paginated({
  daynum,
  count,
}: {
  daynum: string;
  count: number;
}) {
  const day = parseInt(daynum);
  return (
      <Pagination className="mt-4">
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious href={`/schedule/${day > 1 ? day - 1 : 1}`} />
          </PaginationItem>
          {[...Array(count)].map((_, i) => (
            <PaginationItem key={i}>
              <PaginationLink href={`/schedule/${i+1}`}
                isActive={(i + 1) === day}
              >
                {i+1}
              </PaginationLink>
            </PaginationItem>
          ))}
          <PaginationItem>
            <PaginationNext href={`/schedule/${day < count ? day + 1 : count}`} />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
  );
}
