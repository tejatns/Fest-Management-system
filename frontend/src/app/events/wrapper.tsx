import * as React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { useMediaQuery } from "@/hooks/use-media-query";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Label } from "@/components/ui/label";
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
export interface Event {
  id: string;
  name: string;
  date: string;
  venue: string;
  type: string;
  desc: string;
}

export interface Volunteer {
  name: string;
  roll: string;
  dept: string;
}

export interface Participant {
  name: string;
  email: string;
}

export interface Winner {
  name: string;
  position: string;
  prize: string;
}

function extractTime(date: string) {
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "numeric",
  });
}

function extractDate(date: string) {
  return new Date(date).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

export default function DrawerDialogDemo({
  event,
  UserRole,
}: {
  event: Event;
  UserRole: string;
}) {
  const [open, setOpen] = React.useState(false);
  const isDesktop = useMediaQuery("(min-width: 768px)");
  const [VolunteerList, setVolunteerList] = React.useState<Volunteer[]>([]);
  const [ParticipantList, setParticipantList] = React.useState<Participant[]>(
    []
  );
  const [winner, setWinner] = React.useState<Winner[]>([]);
  const [isOrganizer, setIsOrganizer] = React.useState(false);
  const [isVolunteer, setIsVolunteer] = React.useState(false);
  const [isParticipant, setIsParticipant] = React.useState(false);

  React.useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/events/winners/${event.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => {
        if (res.ok) {
          setIsOrganizer(true);
          return res.json();
        } else {
          setIsOrganizer(false);
          return Promise.reject();
        }
      })
      .then((data) => {
        setWinner(data);
      });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  function volunteer(id: string) {
    if (!isVolunteer) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/volunteers/volunteer`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          event_id: id,
        }),
      })
        .then((res) => {
          if (!res.ok) {
            setIsVolunteer(true);
            if (res.status === 409) {
              alert("Already registered as a volunteer");
            } else if (res.status === 406) {
              alert("You are already registered as a participant");
            }
            return Promise.reject();
          }
          return res.json();
        })
        .then((data) => {
          setIsVolunteer(true);
        });
    }
  }

  function register(id: string) {
    if (!isParticipant) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/events/register/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => {
          if (!res.ok) {
            setIsParticipant(true);
            if (res.status === 409) {
              alert("Already registered as a participant");
            } else if (res.status === 406) {
              alert("You are already registered as a volunteer");
            }
            return Promise.reject();
          }
        })
        .then(() => {
          setIsParticipant(true);
        });
    }
  }

  React.useEffect(() => {
    if (UserRole === "organizer") {
      fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/events/registrations/${event.id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      )
        .then((res) => {
          if (res.ok) {
            setIsOrganizer(true);
            return res.json();
          } else {
            setIsOrganizer(false);
            return Promise.reject();
          }
        })
        .then((data) => {
          setParticipantList(data);
        });
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  React.useEffect(() => {
    if (UserRole === "organizer") {
      fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/volunteers/all/${event.id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      )
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            return Promise.reject();
          }
        })
        .then((data) => {
          console.log(data);
          setVolunteerList(data);
        });
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          {/* <Button variant="outline"> */}
          <Card>
            <CardHeader>
              <CardTitle className="font-bold text-xl">{event.name}</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-6">
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="necessary" className="flex flex-col space-y-1">
                  <span>{extractDate(event.date)}</span>
                </Label>
                <span>{extractTime(event.date)}</span>
                {/* <Switch id="necessary" defaultChecked /> */}
              </div>
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="functional" className="flex flex-row space-x-2">
                  <div>Venue:</div>{" "}
                  <div className="font-bold"> {event.venue}</div>
                </Label>
                {/* <Switch id="functional" /> */}
              </div>
              <div className="flex items-center justify-between space-x-2">
                <Label htmlFor="functional" className="flex flex-row space-x-2">
                  <div>Type:</div>{" "}
                  <div className="font-bold"> {event.type}</div>
                </Label>
                {/* <Switch id="functional" /> */}
              </div>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full">
                View Details
              </Button>
            </CardFooter>
          </Card>
          {/* </Button> */}
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle className="font-bold text-xl">
              {event.name}
            </DialogTitle>
            <DialogDescription>{event.desc}</DialogDescription>
          </DialogHeader>
          <form className="grid items-start gap-4">
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="necessary" className="flex flex-col space-y-1">
                <span>{extractDate(event.date)}</span>
              </Label>
              <span>{extractTime(event.date)}</span>
              {/* <Switch id="necessary" defaultChecked /> */}
            </div>
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="functional" className="flex flex-row space-x-2">
                <div>Venue:</div>{" "}
                <div className="font-bold"> {event.venue}</div>
              </Label>
              {/* <Switch id="functional" /> */}
            </div>
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="functional" className="flex flex-row space-x-2">
                <div>Type:</div> <div className="font-bold"> {event.type}</div>
              </Label>
              {/* <Switch id="functional" /> */}
            </div>
            {(UserRole === "participant" || UserRole === "student") && (
              <Button
                type="button"
                onClick={() => register(event.id)}
                disabled={isParticipant}
              >
                Register
              </Button>
            )}
            {UserRole === "student" && (
              <Button
                type="button"
                onClick={() => {
                  volunteer(event.id);
                }}
                disabled={isVolunteer}
              >
                Volunteer
              </Button>
            )}
            {isOrganizer && UserRole === "organizer" && (
              <div className="grid gap-2">
                {VolunteerList.length == 0 && (
                  <>
                    <Separator />
                    <Label
                      htmlFor="username"
                      className="text-sm font-semibold py-2"
                    >
                      No volunteers in this event as of now
                    </Label>
                  </>
                )}
                {VolunteerList.length != 0 && (
                  <>
                    <Separator />
                    <Label htmlFor="username">Volunteers</Label>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="w-[100px]">Name</TableHead>
                          <TableHead>Roll</TableHead>
                          <TableHead>Department</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {VolunteerList.map((volunteer) => (
                          <TableRow key={volunteer.roll}>
                            <TableCell className="font-medium">
                              {volunteer.name}
                            </TableCell>
                            <TableCell className="font-medium">
                              {volunteer.roll}
                            </TableCell>
                            <TableCell className="font-medium">
                              {volunteer.dept}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                      <TableFooter>
                        <TableRow>
                          <TableCell colSpan={3}>Total</TableCell>
                          <TableCell className="text-right">
                            {VolunteerList.length}
                          </TableCell>
                        </TableRow>
                      </TableFooter>
                    </Table>
                  </>
                )}
                {ParticipantList.length == 0 && (
                  //print no empty list
                  <>
                    <Separator />
                    <Label htmlFor="username">No participants as of now</Label>
                  </>
                )}
                {ParticipantList.length != 0 && (
                  <>
                    <Separator />
                    <Label htmlFor="username">Participants</Label>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="w-[100px]">Name</TableHead>
                          <TableHead>Email</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {ParticipantList.map((participant) => (
                          <TableRow key={participant.name}>
                            <TableCell className="font-medium">
                              {participant.name}
                            </TableCell>
                            <TableCell className="font-medium">
                              {participant.email}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                      <TableFooter>
                        <TableRow>
                          <TableCell colSpan={3}>Total</TableCell>
                          <TableCell className="text-right">
                            {ParticipantList.length}
                          </TableCell>
                        </TableRow>
                      </TableFooter>
                    </Table>
                  </>
                )}
              </div>
            )}
            {winner.length != 0 && (
              <>
                <Separator />
                <Label htmlFor="username">Winners</Label>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[100px]">Position</TableHead>
                      <TableHead>Name</TableHead>
                      <TableHead>Prize</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {winner.map((win) => (
                      <TableRow key={win.position}>
                        <TableCell className="font-medium">
                          {win.position}
                        </TableCell>
                        <TableCell className="font-medium">
                          {win.name}
                        </TableCell>
                        <TableCell className="font-medium">
                          {win.prize}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </>
            )}
          </form>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer open={open} onOpenChange={setOpen}>
      <DrawerTrigger asChild>
        {/* <Button variant="outline">Edit Profile</Button>
         */}
        <Card>
          <CardHeader>
            <CardTitle className="font-bold text-xl">{event.name}</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-6">
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="necessary" className="flex flex-col space-y-1">
                <span>{extractDate(event.date)}</span>
              </Label>
              <span>{extractTime(event.date)}</span>
              {/* <Switch id="necessary" defaultChecked /> */}
            </div>
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="functional" className="flex flex-row space-x-2">
                <div>Venue:</div>{" "}
                <div className="font-bold"> {event.venue}</div>
              </Label>
              {/* <Switch id="functional" /> */}
            </div>
            <div className="flex items-center justify-between space-x-2">
              <Label htmlFor="functional" className="flex flex-row space-x-2">
                <div>Type:</div> <div className="font-bold"> {event.type}</div>
              </Label>
              {/* <Switch id="functional" /> */}
            </div>
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full">
              View Details
            </Button>
          </CardFooter>
        </Card>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader className="text-left">
          <DrawerTitle className="font-bold text-xl">{event.name}</DrawerTitle>
          <DrawerDescription>{event.desc}</DrawerDescription>
        </DrawerHeader>
        {/* <ProfileForm className="px-4" /> */}
        <form className="px-4 grid items-start gap-4">
          <div className="flex items-center justify-between space-x-2">
            <Label htmlFor="necessary" className="flex flex-col space-y-1">
              <span>{extractDate(event.date)}</span>
            </Label>
            <span>{extractTime(event.date)}</span>
            {/* <Switch id="necessary" defaultChecked /> */}
          </div>
          <div className="flex items-center justify-between space-x-2">
            <Label htmlFor="functional" className="flex flex-row space-x-2">
              <div>Venue:</div> <div className="font-bold"> {event.venue}</div>
            </Label>
            {/* <Switch id="functional" /> */}
          </div>
          <div className="flex items-center justify-between space-x-2">
            <Label htmlFor="functional" className="flex flex-row space-x-2">
              <div>Type:</div> <div className="font-bold"> {event.type}</div>
            </Label>
            {/* <Switch id="functional" /> */}
          </div>

          {(UserRole === "participant" || UserRole === "student") && (
            <Button
              type="button"
              onClick={() => register(event.id)}
              disabled={isParticipant}
            >
              Register
            </Button>
          )}
          {UserRole === "student" && (
            <Button
              type="button"
              onClick={() => {
                volunteer(event.id);
              }}
              disabled={isVolunteer}
            >
              Volunteer
            </Button>
          )}
          {isOrganizer && UserRole === "organizer" && (
            <div className="grid gap-2">
              {VolunteerList.length == 0 && (
                <>
                  <Separator />
                  <Label
                    htmlFor="username"
                    className="text-sm font-semibold py-2"
                  >
                    No volunteers in this event as of now
                  </Label>
                </>
              )}
              {VolunteerList.length != 0 && (
                <>
                  <Separator />
                  <Label htmlFor="username">Volunteers</Label>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-[100px]">Name</TableHead>
                        <TableHead>Roll</TableHead>
                        <TableHead>Department</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {VolunteerList.map((volunteer) => (
                        <TableRow key={volunteer.roll}>
                          <TableCell className="font-medium">
                            {volunteer.name}
                          </TableCell>
                          <TableCell className="font-medium">
                            {volunteer.roll}
                          </TableCell>
                          <TableCell className="font-medium">
                            {volunteer.dept}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                    <TableFooter>
                      <TableRow>
                        <TableCell colSpan={3}>Total</TableCell>
                        <TableCell className="text-right">
                          {VolunteerList.length}
                        </TableCell>
                      </TableRow>
                    </TableFooter>
                  </Table>
                </>
              )}
              {ParticipantList.length == 0 && (
                //print no empty list
                <>
                  <Separator />
                  <Label htmlFor="username">No participants as of now</Label>
                </>
              )}
              {ParticipantList.length != 0 && (
                <>
                  <Separator />
                  <Label htmlFor="username">Participants</Label>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-[100px]">Name</TableHead>
                        <TableHead>Email</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {ParticipantList.map((participant) => (
                        <TableRow key={participant.name}>
                          <TableCell className="font-medium">
                            {participant.name}
                          </TableCell>
                          <TableCell className="font-medium">
                            {participant.email}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                    <TableFooter>
                      <TableRow>
                        <TableCell colSpan={3}>Total</TableCell>
                        <TableCell className="text-right">
                          {ParticipantList.length}
                        </TableCell>
                      </TableRow>
                    </TableFooter>
                  </Table>
                </>
              )}
            </div>
          )}
          {winner.length != 0 && (
            <>
              <Separator />
              <Label htmlFor="username">Winners</Label>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[100px]">Position</TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Prize</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {winner.map((win) => (
                    <TableRow key={win.position}>
                      <TableCell className="font-medium">
                        {win.position}
                      </TableCell>
                      <TableCell className="font-medium">{win.name}</TableCell>
                      <TableCell className="font-medium">{win.prize}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          )}
        </form>
      </DrawerContent>
    </Drawer>
  );
}
