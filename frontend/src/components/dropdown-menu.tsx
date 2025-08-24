"use client";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import React from "react";

export function ProfileDropdown({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [role, setRole] = React.useState<
    "student" | "organizer" | "admin" | "participant" | null
  >(null);

  React.useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/role`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setRole(data.role);
        });
    }
  }, []);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>{children}</DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuLabel>My Account</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem
            className="cursor-pointer"
            onClick={() => {
              // redirect to profile
              window.location.href = "/profile";
            }}
          >
            <span>Profile</span>
            {/* <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut> */}
          </DropdownMenuItem>
          {role === "admin" && (
            <DropdownMenuItem
              className="cursor-pointer"
              onClick={() => {
                // redirect to admin
                window.location.href = "/admin";
              }}
            >
              <span>Admin</span>
              {/* <DropdownMenuShortcut>⇧⌘A</DropdownMenuShortcut> */}
            </DropdownMenuItem>
          )}
        </DropdownMenuGroup>
        <DropdownMenuItem
          className="cursor-pointer"
          onClick={() => {
            // log out
            localStorage.removeItem("token");
            window.location.href = "/";
          }}
        >
          <span>Log out</span>
          {/* <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut> */}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
