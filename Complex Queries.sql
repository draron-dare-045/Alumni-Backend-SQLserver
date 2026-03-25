USE Alumnidb;
GO
--COMPLEX QUERIES

--1. Alumni Directory By Graduation Year
SELECT AlumniID, FirstName, LastName, GraduationYear, Degree, Email
FROM AlumniDetails
WHERE GraduationYear = 2024
ORDER BY LastName, FirstName;
GO

--2. Alumni Directory By Chapter
SELECT AlumniID,FirstName,LastName,ChapterID,Degree,Email
FROM AlumniDetails
WHERE ChapterID=3
ORDER BY LastName,FirstName;
GO

--3. Total Donations Per Event
SELECT Events.EventName AS "Event Name",SUM(Donations.Amount) AS "Total Donations"
FROM Events
LEFT OUTER JOIN Donations ON Events.EventID = Donations.EventID
GROUP BY Events.EventName
ORDER BY "Total Donations" DESC;
GO

--4. Award Winners By Year
SELECT W.AwardYear, A.FirstName, A.LastName, W.AwardName
FROM Awards W
INNER JOIN AlumniDetails A ON W.AlumniID = A.AlumniID
ORDER BY W.AwardYear DESC;
GO

--5. Event Participation List
SELECT A.FirstName, A.LastName, E.EventName, EP.Role
FROM EventParticipation EP
INNER JOIN AlumniDetails A ON EP.AlumniID = A.AlumniID
INNER JOIN Events E ON EP.EventID = E.EventID
ORDER BY E.EventName;
GO

--6. Program Participation List
SELECT A.FirstName, A.LastName, P.ProgramName, PP.Role
FROM ProgramParticipation PP
JOIN AlumniDetails A ON PP.AlumniID = A.AlumniID
JOIN AlumniPrograms P ON PP.ProgramID = P.ProgramID
ORDER BY P.ProgramName;

--Further Complex Queries

--7. Alumni Who Participated in Both Events and Programs
SELECT FirstName,LastName
FROM AlumniDetails
WHERE AlumniID IN(SELECT AlumniID FROM EventParticipation) AND 
AlumniID IN (SElECT AlumniID FROM ProgramParticipation);
GO

--8. Top Donor(Highest Contributor)
SELECT TOP 1 A.FirstName,A.LastName,SUM(D.Amount) AS "Total Donations"
FROM AlumniDetails A
JOIN Donations D on A.AlumniID=D.AlumniID
GROUP BY A.FirstName,A.LastName
ORDER BY "Total Donations" DESC;
GO

--9. Events with Number of Participants
SELECT E.EventName,COUNT(EP.AlumniID) as "Number of Participants"
FROM Events E
LEFT OUTER JOIN EventParticipation EP ON E.EventID=EP.EventID
GROUP BY E.EventName;
GO

--10. Alumni Participation Summary (Events And Programs)
SELECT A.FirstName, A.LastName,
       COUNT(DISTINCT EP.EventID) AS EventsParticipated,
       COUNT(DISTINCT PP.ProgramID) AS ProgramsParticipated
FROM AlumniDetails A
LEFT OUTER JOIN EventParticipation EP ON A.AlumniID = EP.AlumniID
LEFT OUTER JOIN ProgramParticipation PP ON A.AlumniID = PP.AlumniID
GROUP BY A.FirstName, A.LastName;
GO

--11. Instituitions with Most Collaborations
SELECT I.InstitutionName, COUNT(C.CollaborationID) AS TotalCollaborations
FROM ExternalInstitutions I
INNER JOIN CollaborationActivities C ON I.InstitutionID = C.InstitutionID
GROUP BY I.InstitutionName
ORDER BY TotalCollaborations DESC;
GO

--12. Alumni and Their Latest Donation
SELECT A.FirstName, A.LastName, D.Amount, D.DonationDate
FROM AlumniDetails A
JOIN Donations D ON A.AlumniID = D.AlumniID
WHERE D.DonationDate = (
    SELECT MAX(D2.DonationDate)
    FROM Donations D2
    WHERE D2.AlumniID = A.AlumniID);
GO    
--13. Programs with No Participants
SELECT P.ProgramName,P.ProgramID
FROM AlumniPrograms P
LEFT JOIN ProgramParticipation PP ON P.ProgramID=PP.ProgramID
WHERE PP.ProgramID IS NULL;
GO

--14. Total Donations Per Alumni
SELECT A.AlumniID, A.FirstName, A.LastName,
ISNULL(SUM(D.Amount), 0) AS TotalDonations
FROM AlumniDetails A
LEFT JOIN Donations D ON A.AlumniID = D.AlumniID
GROUP BY A.AlumniID, A.FirstName, A.LastName;
GO

--15. Events with Donations Above Average
SELECT E.EventName, SUM(D.Amount) AS TotalDonations
FROM Events E
JOIN Donations D ON E.EventID = D.EventID
GROUP BY E.EventName
HAVING SUM(D.Amount) > (
    SELECT AVG(Amount) FROM Donations
);
GO
--16. Basic View for All Alumni
CREATE VIEW vw_AllAlumni AS
SELECT AlumniID, FirstName, LastName, Email, GraduationYear
FROM AlumniDetails;
GO

--17.Alumni with Full Names
CREATE VIEW vw_AlumniFullName AS
SELECT AlumniID,
       FirstName + ' ' + LastName AS FullName,
       Email
FROM AlumniDetails;
GO

--18. Events Summary
CREATE VIEW vw_EventSummary AS
SELECT EventID, EventName, EventDate, Location
FROM Events;
GO

--19. Donations with Event Info
CREATE VIEW vw_DonationsWithEvents AS
SELECT D.DonationID, D.Amount, D.DonationDate, E.EventName
FROM Donations D
INNER JOIN Events E ON D.EventID = E.EventID;
GO

--20. Total Donations per Event
CREATE VIEW vw_TotalDonationsPerEvent AS
SELECT E.EventID, E.EventName, SUM(D.Amount) AS TotalDonations
FROM Events E
LEFT JOIN Donations D ON E.EventID = D.EventID
GROUP BY E.EventID, E.EventName;
GO

--21. Alumni Participation in Events
CREATE VIEW vw_AlumniEventParticipation AS
SELECT A.AlumniID, A.FirstName, A.LastName, E.EventName
FROM AlumniDetails A
INNER JOIN EventParticipation EP ON A.AlumniID = EP.AlumniID
INNER JOIN Events E ON EP.EventID = E.EventID;
GO

--22.Alumni Contact List
CREATE VIEW vw_AlumniContacts AS
SELECT FirstName, LastName, Email, Phone
FROM AlumniDetails;
GO

--23. Events with Number of Participants
CREATE VIEW vw_EventParticipantCount AS
SELECT E.EventID, E.EventName, COUNT(EP.AlumniID) AS TotalParticipants
FROM Events E
LEFT JOIN EventParticipation EP ON E.EventID = EP.EventID
GROUP BY E.EventID, E.EventName;
GO

--24. High Value donations above 1000
CREATE VIEW vw_HighValueDonations AS
SELECT DonationID, AlumniID, Amount, DonationDate
FROM Donations
WHERE Amount > 1000;
GO

--25. Alumni Donations Summary
CREATE VIEW vw_AlumniDonationSummary AS
SELECT A.AlumniID, A.FirstName, A.LastName, SUM(D.Amount) AS TotalDonated
FROM AlumniDetails A
LEFT JOIN Donations D ON A.AlumniID = D.AlumniID
GROUP BY A.AlumniID, A.FirstName, A.LastName;
GO

--26. Events in a Specific Year
CREATE VIEW vw_EventsByYear AS
SELECT EventID, EventName, EventDate
FROM Events
WHERE YEAR(EventDate) = 2025;
GO

--27. Alumni Who Have Not Donated
CREATE VIEW vw_NonDonors AS
SELECT A.AlumniID, A.FirstName, A.LastName
FROM AlumniDetails A
LEFT JOIN Donations D ON A.AlumniID = D.AlumniID
WHERE D.DonationID IS NULL;
GO

--28. Event Donations Detail
CREATE VIEW vw_EventDonationDetails AS
SELECT E.EventName, D.DonationID, D.Amount, D.DonationDate
FROM Events E
INNER JOIN Donations D ON E.EventID = D.EventID;
GO

--29. Donations Per Month
CREATE VIEW vw_MonthlyDonations AS
SELECT YEAR(DonationDate) AS Year,
       MONTH(DonationDate) AS Month,
       SUM(Amount) AS TotalAmount
FROM Donations
GROUP BY YEAR(DonationDate), MONTH(DonationDate);
GO

--30. Alumni Participation Summary
CREATE VIEW vw_AlumniParticipationSummary AS
SELECT A.AlumniID, A.FirstName, A.LastName, COUNT(EP.EventID) AS EventsAttended
FROM AlumniDetails A
LEFT JOIN EventParticipation EP ON A.AlumniID = EP.AlumniID
GROUP BY A.AlumniID, A.FirstName, A.LastName;
GO





