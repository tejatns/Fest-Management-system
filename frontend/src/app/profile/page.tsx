"use client";

import * as React from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar } from "@radix-ui/react-avatar";
import { AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Optional } from "utility-types";

type ProfileFormValues = Optional<{
  name: string;
  email: string;
  phone: string;
  dept: string;
  university: string;
  roll: string;
  accomodation: string;
  mess: string;
}>;

export default function Profile() {
  const [values, setValues] = React.useState<ProfileFormValues>(
    {} as ProfileFormValues
  );
  const [role, setRole] = React.useState<string>("" as string);

  React.useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setValues(data);
          setRole(data.role);
        });
    }
  }, []);

  function getProfile(role: string) {
    if (role === "participant") {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/participants/me`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setValues(
            values => ({ 
              ...values, 
              university: data.university,
              dept: undefined,
              roll: undefined,
              accomodation: data.accomodation,
              mess: data.mess,
            })
          );
        });
    }

    if (role === "student") {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/students/me`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setValues(
            values => ({
              ...values, 
              dept: data.dept, 
              roll: data.roll,
              university: undefined,
              accomodation: undefined,
              mess: undefined,
            })
          );
        });
    }
  }

  React.useEffect(() => {
    getProfile(role);
  }, [role]);

  return (
    <main className="flex items-center justify-center h-screen">
      <Card className="w-[350px]">
        <CardHeader
          className="flex items-center justify-between flex-row"
          title="Profile"
        >
          <div>
            <CardTitle>Profile</CardTitle>
            <CardDescription>Relevant Details</CardDescription>
          </div>
          <Avatar className="ml-2 w-12 h-12">
            <AvatarImage src="https://github.com/shadcn.png" alt="@denormies" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4">
              {values.name && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    placeholder="Name"
                    defaultValue={values.name}
                    disabled
                  />
                </div>
              )}
              {values.email && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    placeholder="Email"
                    defaultValue={values.email}
                    disabled
                  />
                </div>
              )}
              {values.phone && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="phone">Phone</Label>
                  <Input
                    id="phone"
                    placeholder="Phone"
                    defaultValue={values.phone}
                    disabled
                  />
                </div>
              )}
              {values.roll && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="roll">Roll</Label>
                  <Input
                    id="roll"
                    placeholder="Roll"
                    defaultValue={values.roll}
                    disabled
                  />
                </div>
              )}
              {values.dept && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="dept">Department</Label>
                  <Input
                    id="dept"
                    placeholder="Department"
                    defaultValue={values.dept}
                    disabled
                  />
                </div>
              )}
              {values.university && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="university">University</Label>
                  <Input
                    id="university"
                    placeholder="University"
                    defaultValue={values.university}
                    disabled
                  />
                </div>
              )}
              {values.accomodation && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="accomodation">Accomodation</Label>
                  <Input
                    id="accomodation"
                    placeholder="Accomodation"
                    defaultValue={values.accomodation}
                    disabled
                  />
                </div>
              )}
              {values.mess && (
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="mess">Mess</Label>
                  <Input
                    id="mess"
                    placeholder="Mess"
                    defaultValue={values.mess}
                    disabled
                  />
                </div>
              )}
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="destructive">Delete Account</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Are You Really Sure?</DialogTitle>
                <DialogDescription>
                  This will permanently delete your account.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter className="sm:mt-8">
                <DialogClose asChild>
                  <Button variant="ghost">Cancel</Button>
                </DialogClose>
                <Button
                  variant="destructive"
                  onClick={() => {
                    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/me`, {
                      method: "DELETE",
                      headers: {
                        Authorization: `Bearer ${localStorage.getItem(
                          "token"
                        )}`,
                      },
                    }).then(() => {
                      localStorage.removeItem("token");
                      window.location.href = "/auth";
                    });
                  }}
                >
                  Delete
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
          <Button
            variant="secondary"
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/";
            }}
          >
            Log out
          </Button>
        </CardFooter>
      </Card>
    </main>
  );
}
