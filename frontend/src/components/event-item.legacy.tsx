import Image from "next/image";
import { PlusCircledIcon } from "@radix-ui/react-icons";

import { cn } from "@/lib/utils";

export interface Event {
  name: string
  desc: string
  thumbnail: string
}

interface EventItemProps extends React.HTMLAttributes<HTMLDivElement> {
  event: Event;
  aspectRatio?: "portrait" | "square";
  width?: number;
  height?: number;
}

export function EventItem({
  event,
  aspectRatio = "portrait",
  width,
  height,
  className,
  ...props
}: EventItemProps) {
  return (
    <div className={cn("space-y-3", className)} {...props}>
      <div className="overflow-hidden rounded-md">
        <Image
          src={event.thumbnail}
          alt={event.name}
          width={width}
          height={height}
          className={cn(
            "h-auto w-auto object-cover transition-all hover:scale-105",
            aspectRatio === "portrait" ? "aspect-[3/4]" : "aspect-square"
          )}
        />
      </div>
      <div className="space-y-1 text-sm">
        <h3 className="font-medium leading-none">{event.name}</h3>
        <p className="text-xs text-muted-foreground">{event.desc}</p>
      </div>
    </div>
  );
}
