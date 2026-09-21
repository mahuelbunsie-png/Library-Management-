# Library Member (Patron) - Joint Requirements

**Group:** 27  
**Project:** Library Management  
**Stakeholder:** Library Member (Patron)  
**Role Type:** Shared Role

## Stakeholder Summary

The Library Member is a regular patron of Riverside Public Library who
frequently borrows books for both themselves and their children.

The Member's main priorities are convenience, being able to access library
information without visiting the front desk, keeping track of borrowed books
and their due dates, and having more flexibility when a desired book is
unavailable or when additional borrowing time is needed.

The Member wants to check from home whether a book is available before making
a trip to the library. They also want to see which books they currently have
checked out and when those books are due without having to ask front-desk
staff.

If a desired book is already checked out, the Member wants to place a hold so
they can be next in line when the book is returned. The Member also wants to
renew borrowed books when additional time is needed, provided that another
member is not waiting for the book.

The Member does not want to create another account with a complicated
password and would prefer access to be tied to their existing library card
number.

A major concern for the Member is the handling of overdue books. The Member is
strongly opposed to late fines and would prefer a friendly reminder before the
due date or a short grace period.

## Joint Requirements

### Functional Requirements

**MEM-01:** The system shall allow library members to remotely check whether a
book is currently available.

**MEM-02:** The system shall allow library members to view the books they
currently have checked out.

**MEM-03:** The system shall display the due date of each book currently
checked out by a library member.

**MEM-04:** The system shall allow a library member to place a hold on a book
that is currently checked out.

**MEM-05:** The system shall place a member who has a hold on a checked-out
book in line to receive the book when it becomes available.

**MEM-06:** The system shall send library members a reminder before a borrowed
book reaches its due date.

**MEM-07:** The system shall support a grace period for overdue books before an
overdue consequence is applied.

**MEM-08:** The system shall allow library members to access their library
information using their library card number.

**MEM-09:** The system shall allow a library member to renew a borrowed book
when no other member is waiting for that book.

**MEM-10:** The system shall prevent a library member from renewing a borrowed
book when another member is waiting for that book.

## Stakeholder Rationale

### Remote Book Availability

The Member wants to check whether a desired book is available before making a
trip to the library.

The system should therefore make current book availability information
accessible remotely. This would allow the Member to determine whether a book
is available without first travelling to the library.

### Borrowed Books and Due Dates

The Member wants to see which books they currently have checked out and the
due date of each book without having to ask someone at the front desk.

The Member has previously lost track of due dates because there was no
reminder. Providing access to current loans and their due dates would make it
easier for the Member to keep track of borrowed material.

### Book Holds

If a desired book is currently checked out, the Member wants to be able to
place a hold on it.

The Member wants to be next in line when the book is returned instead of
having to repeatedly check whether the book has become available.

### Due-Date Reminders

The Member wants to receive a friendly reminder before a borrowed book reaches
its due date.

This is important to the Member because they have previously lost track of due
dates when there was no reminder. A reminder would give the Member an
opportunity to return or renew the book before it becomes overdue.

### Renewals

The Member sometimes wants to keep a borrowed book for longer instead of
returning it immediately.

The Member wants to be able to renew a book as long as another member is not
waiting for it. If another member is waiting for the book, the current borrower
should not be able to renew it.

### Member Access

The Member does not want to create another account with a complicated
password.

The Member would prefer access to their library information to be tied to
their existing library card number.

### Overdue Books

The Member strongly opposes late fines.

From the Member's perspective, a person may return a book late because of work
or family schedules rather than because they are careless. The Member believes
that fines may unfairly punish people who are already busy or dealing with
other responsibilities.

Instead of fines, the Member would prefer a friendly reminder before the due
date or a short grace period.

## Unresolved and Unspecified Details

Several needs identified from the Library Member role require additional
clarification. These details have intentionally not been invented because they
were not specified by the stakeholder.

**MEM-04 and MEM-05 - Book holds:**  
The Member wants to be next in line for a checked-out book. However, the
stakeholder does not specify how the system should handle multiple members
waiting for the same book.

The stakeholder also does not specify how long a returned book should be held
for a member before becoming available to someone else.

**MEM-06 - Due-date reminder:**  
The Member wants a friendly reminder before the due date, but the stakeholder
does not specify how far in advance the reminder should be sent.

The stakeholder also does not specify how the reminder should be delivered.

**MEM-07 - Grace period:**  
The Member requests a "short grace period," but the exact length of the grace
period is not specified.

**MEM-08 - Library card access:**  
The Member wants access tied to their library card number and does not want a
complicated password. However, the stakeholder does not fully specify how
authentication should work or whether any additional information should be
required to access an account.

**MEM-09 and MEM-10 - Renewals:**  
The Member wants to renew a book as long as nobody else is waiting for it.
However, the stakeholder does not specify how many times a book may be renewed
or whether there should be any other restrictions on renewals.

These unresolved details should be considered during requirements analysis
and the requirements quality check rather than resolved by making assumptions.

## Identified Stakeholder Conflict

### Overdue Book Policy

A significant conflict exists between the Library Member and the Librarian
regarding how overdue books should be handled.

The Library Member strongly opposes late fines. The Member believes that books
may be returned late because of work and family schedules rather than
carelessness and believes fines can unfairly punish patrons.

The Member would prefer a friendly reminder before the due date or a short
grace period instead of being charged money.

The Librarian takes a different position. The Librarian strongly believes that
overdue books should have a consequence and prefers a small daily fine. From
the Librarian's perspective, late returns are a major complaint from members
waiting for books, and fines encourage books to be returned on time.

The Library Director is aware that staff and patrons may disagree about fines.
The Director is open to some consequence for chronically late returns but is
concerned about anything that may feel punitive to lower-income patrons.

The Director has not made a final decision on the policy. If required to
express a preference, the Director is currently leaning toward a small grace
period followed by a modest fine only after repeated lateness, but this is not
a final decision.

Therefore, the group has documented the overdue-book policy as an open
stakeholder conflict rather than selecting one stakeholder's preferred
solution.

The conflict should be addressed during requirements analysis and
consolidation.

## Joint Elicitation Summary

The Library Member requirements focus on making the library system more
convenient and accessible to patrons.

The Member wants to remotely check whether books are available, see currently
borrowed books and their due dates, place holds on unavailable books, receive
due-date reminders, and renew books when another member is not waiting for
them.

The Member also wants access to be connected to their existing library card
number rather than requiring another complicated account.

The joint elicitation identified several details that require further
clarification, including the timing and delivery method of reminders, the
length of a grace period, the handling of multiple holds, renewal limits, and
the exact authentication process.

The most significant stakeholder conflict concerns overdue-book policy. The
Member strongly opposes fines, while the Librarian strongly supports a small
daily fine. The Library Director has not made a final policy decision.

This conflict has intentionally been left unresolved so that the positions of
all stakeholders can be preserved and considered during requirements analysis
and consolidation.
