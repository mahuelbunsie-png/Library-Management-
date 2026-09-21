# Librarian (Front-Desk Staff) - Individual Requirements

**Group:** 27  
**Project:** Library Management  
**Stakeholder:** Librarian (Front-Desk Staff)  
**Role Type:** Primary Role

## Stakeholder Summary

The Librarian works at the front desk of Riverside Public Library and is
responsible for checking books in and out, answering questions, and handling
the day-to-day activities of the library.

The Librarian's main concerns with the current process are speed, simplicity,
and the accuracy of book availability information. The current spreadsheet can
be a day behind, making it difficult to determine whether a book is actually
available or checked out.

The Librarian often has 2 to 3 people waiting at the front desk and therefore
needs to find information and complete transactions quickly. Since the
Librarian is not especially comfortable with computers, the system should
also be simple to use and require few steps for common transactions.

The Librarian also considers overdue books a significant problem because late
returns prevent other members from accessing books they are waiting for. The
Librarian believes overdue books should have a consequence and specifically
prefers a small daily fine.

## Individual Requirements

### Functional Requirements

**LIB-01:** The system shall allow front-desk staff to search for books by
title.

**LIB-02:** The system shall allow front-desk staff to search for books by
author.

**LIB-03:** The system shall allow front-desk staff to search for library
members by name.

**LIB-04:** The system shall display whether a book is currently available or
checked out.

**LIB-05:** The system shall update a book's availability status when the book
is checked out.

**LIB-06:** The system shall update a book's availability status when the book
is returned.

**LIB-07:** The system shall allow front-desk staff to check out books to
library members.

**LIB-08:** The system shall allow front-desk staff to check in returned books.

**LIB-09:** The system shall automatically inform front-desk staff when a
member being served has an overdue book.

**LIB-10:** The system shall support applying a small daily fine to overdue
books.

### Non-Functional Requirements

**LIB-11:** The system shall allow front-desk staff to look up a book or
library member within a few seconds.

**LIB-12:** The system shall provide a simple interface for front-desk staff
who are not especially comfortable with computers.

**LIB-13:** The system shall allow common front-desk transactions to be
completed using few steps.

## Stakeholder Rationale

### Search and Lookup

The Librarian needs to find books and members quickly while working at the
front desk. Books should be searchable by title and author, while members
should be searchable by name because members may not always remember their
exact library ID.

### Book Availability

The current spreadsheet can be a day behind, so the Librarian cannot always
trust the displayed availability of a book. The new system should maintain
up-to-date information when books are checked out and returned so that staff
can accurately determine whether a book is available.

### Front-Desk Efficiency

The Librarian frequently has 2 to 3 people waiting at the front desk. As a
result, speed is more important to this stakeholder than visually attractive
screens. Common transactions should be simple and require few steps.

### Overdue Books

The Librarian wants to be automatically informed when a member being served
has an overdue book. This would prevent the Librarian from having to manually
search for overdue items.

The Librarian also believes overdue books should have a consequence because
late returns prevent other members from accessing books they are waiting for.
The Librarian's preferred consequence is a small daily fine. The Librarian is
willing to compromise on the amount of the fine but does not want the need for
an overdue consequence to be removed.

## Unresolved and Unspecified Details

Several needs identified during elicitation require additional clarification.
These details have intentionally not been invented because they were not
specified by the stakeholder.

**LIB-10 - Small daily fine:**  
The Librarian requested a "small daily fine," but the exact amount of the fine
was not specified.

**LIB-11 - Lookup speed:**  
The Librarian wants to find a book or member "within a few seconds," but an
exact maximum response time was not specified.

**LIB-12 - Simple interface:**  
The Librarian described the desired system as simple to use, but "simple" does
not provide a measurable usability criterion.

**LIB-13 - Few steps:**  
The Librarian wants common transactions to require "few steps," but the
maximum acceptable number of steps was not specified.

These details should be considered during requirements analysis and the
requirements quality check.

## Identified Stakeholder Conflict

### Overdue Book Policy

The Librarian's preference for a small daily fine creates a conflict with the
Library Member stakeholder.

The Librarian believes overdue books require a consequence and prefers a small
daily fine because late returns prevent other members from accessing books
they are waiting for.

The Library Member is strongly opposed to late fines and instead prefers a
friendly reminder before the due date or a short grace period.

The Library Director is aware that staff and patrons may disagree on the fines
question but has not made a final decision. The Director is open to some
consequence for chronically late returns but is concerned about policies that
may feel punitive to lower-income patrons.

Therefore, the overdue-book policy remains an open stakeholder conflict. The
Librarian's preference for a small daily fine has been retained in this
individual requirements list because it accurately represents this
stakeholder's position. The conflict should be addressed during consolidation
rather than resolved by removing one stakeholder's requirement.

## Elicitation Summary

The Librarian's requirements focus primarily on improving the efficiency and
accuracy of front-desk operations.

The stakeholder needs to search for books and members quickly, see accurate
book availability information, efficiently check books in and out, and be
automatically informed about overdue books.

The Librarian also requires a system that is simple to use because they are
not especially comfortable with computers and frequently need to serve
multiple people waiting at the front desk.

The elicitation also identified an unresolved policy conflict concerning
overdue books. The Librarian supports a small daily fine, while the Library
Member opposes fines. This disagreement has intentionally been preserved for
the later requirements analysis and consolidation stage.
