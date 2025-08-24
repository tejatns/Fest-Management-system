"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { ZodType, z } from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Popover, PopoverTrigger } from "./ui/popover";
import { cn } from "@/lib/utils";
import { CaretSortIcon, CheckIcon } from "@radix-ui/react-icons";
import { PopoverContent } from "@radix-ui/react-popover";
import { Command, CommandGroup, CommandItem } from "./ui/command";

type FormSchema = {
  name: string;
  email: string;
  phone: string;
  password: string;
  confirmPassword: string;
  role: string;
  roll?: string;
  department?: string;
  university?: string;
};

const formSchema: ZodType<FormSchema> = z
  .object({
    name: z.string().min(2, "Name must be at least 2 characters"),
    email: z.string().email(),
    phone: z.string(),
    password: z.string().min(4, "Password must be at least 4 characters"),
    confirmPassword: z.string(),
    role: z.string(),
    roll: z.string().optional(),
    department: z.string().optional(),
    university: z.string().optional(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"], // path of error
  })
  .refine((data) => data.phone === "" || data.phone.length === 10, {
    message: "Phone number must be 10 digits",
    path: ["phone"],
  });

type Roles = {
  value: string;
  label: string;
};

const roles: Roles[] = [
  {
    value: "student",
    label: "Student",
  },
  {
    value: "participant",
    label: "Participant",
  },
  {
    value: "organizer",
    label: "Organizer",
  },
  {
    value: "sponsor",
    label: "Sponsor",
  },
];

export function SignupForm() {
  
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    
    defaultValues: {
      name: "",
      email: "",
      phone: "",
      password: "",
      confirmPassword: "",
      role: "participant",
    },
  });
  
  const [initSignUp, setInitSignUp] = React.useState(false);
  function onSubmit(values: z.infer<typeof formSchema>) {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: values.name,
        email: values.email,
        phone: (values.phone === "" ? undefined : values.phone), 
        password: values.password,
        role: values.role,
      }),
    })
      .then((res) => {
        if (!res.ok) {
          res.json().then((data) => {
            form.setError("email", {
              type: "manual",
              message: data.detail,
            });
          });
          return Promise.reject();
        }
        return res.json();
      })
      .then((data) => {
        localStorage.setItem("token", data.token);
        setInitSignUp(true);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  React.useEffect(() => {
    if (initSignUp) {
      if (form.watch("role") === "students") {
        fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/students/me`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            roll: form.watch("roll"),
            department: form.watch("department"),
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            window.location.href = "/";
          });
      } else if (form.watch("role") === "participant") {
        fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/participants/me`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            university: form.watch("university"),
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            window.location.href = "/";
          });
      }
      else window.location.href = "/";
    }
  }, [initSignUp]); // eslint-disable-line react-hooks/exhaustive-deps

  const [open, setOpen] = React.useState(false);

  return (
    <Card>
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Create an account</CardTitle>
        <CardDescription>
          Enter the details below to create your account
        </CardDescription>
      </CardHeader>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
          <CardContent className="grid gap-2">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="John Doe" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="abc.example.com" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="phone"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Phone</FormLabel>
                  <FormControl>
                    <Input placeholder="0000000000" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {/* ------------------------------ Drop Down --------------------------------- */}
            <FormField
              control={form.control}
              name="role"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel>Role</FormLabel>
                  <Popover open={open} onOpenChange={setOpen}>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className={cn(
                            "w-[200px] justify-between",
                            !field.value && "text-muted-foreground"
                          )}
                        >
                          {field.value
                            ? roles.find((role) => role.value === field.value)
                                ?.label
                            : "Select Role"}
                          <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-[200px] p-0 text-green-500">
                      <Command>
                        {/* <CommandInput
                          placeholder="Search framework..."
                          className="h-9"
                        />
                        <CommandEmpty>No framework found.</CommandEmpty> */}
                        <CommandGroup className="border-[1px] rounded-md shadow-md">
                          {roles.map((role) => (
                            <CommandItem
                              value={role.label}
                              key={role.value}
                              onSelect={() => {
                                form.setValue("role", role.value);
                                setOpen(false);
                              }}
                            >
                              {role.label}
                              <CheckIcon
                                className={cn(
                                  "ml-auto h-4 w-4",
                                  role.value === field.value
                                    ? "opacity-100"
                                    : "opacity-0"
                                )}
                              />
                            </CommandItem>
                          ))}
                        </CommandGroup>
                      </Command>
                    </PopoverContent>
                  </Popover>
                  <FormMessage />
                </FormItem>
              )}
            />
            {form.watch("role") === "student" && (
              <FormField
                control={form.control}
                name="roll"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Roll</FormLabel>
                    <FormControl>
                      <Input placeholder="123456" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            {form.watch("role") === "student" && (
              <FormField
                control={form.control}
                name="department"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Department</FormLabel>
                    <FormControl>
                      <Input placeholder="CSE" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            {form.watch("role") === "participant" && (
              <FormField
                control={form.control}
                name="university"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>University</FormLabel>
                    <FormControl>
                      <Input placeholder="IIT" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            {/* ------------------------------ Password --------------------------------- */}
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input placeholder="********" {...field} type="password" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="confirmPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <Input placeholder="********" {...field} type="password" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </CardContent>
          <CardFooter>
            <Button type="submit">Create account</Button>
          </CardFooter>
        </form>
      </Form>
    </Card>
  );
}
