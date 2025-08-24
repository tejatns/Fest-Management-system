import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ProfileDropdown } from "./dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export default function LoginOrProfile() {
    let token = null;
    if (typeof window !== "undefined") {
      token = localStorage.getItem("token");
    }
  
    if (token) {
      return (
        <Link href="/">
          <ProfileDropdown>
            <Avatar className="ml-2 cursor-pointer">
              <AvatarImage src="https://github.com/shadcn.png" alt="@denormies" />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
          </ProfileDropdown>
        </Link>
      );
    }
    else {
      return (
        <Link href="/auth">
          <Button variant="secondary" className="ml-2">
            Log in
          </Button>
        </Link>
      );
    }
  }