USE Alumnidb;
GO

INSERT INTO AlumniDetails
(FirstName, Lastname, Gender, Dateofbirth, GraduationYear, Degree, Email, Phone, ChapterId)
VALUES
('John','Mwangi','Male','1992-08-22',2016,'Information Technology','john@gmail.com','0723457890', 1),
('Faith','Buyale','Female','2001-01-01',2025,'Bachelor of Commerce','fbuyale@gmail.com','0134526772',3),
('Mary', 'Mutheu', 'Female', '2000-03-10', 2024, 'Software Engineering', 'mary@gmail.com', '0734567890', 2),
('David', 'Otieno', 'Male', '1996-11-05', 2020, 'Actuarial Science', 'david@mail.com', '0745678901', 6),
('Alice','Abdul','Female','1999-05-04',2021,'Political Science','aliceabdul@gmail.com','0722334455',4),
('Peter','Roberts','Male','1991-12-25',2015,'Civil Engineering','roberts@gmail.com','0709876543',5),
('James','Kamau','Male','1993-07-15',2017,'Mechanical Engineering','jkamau@gmail.com','0721123344',2),
('Grace','Wanjiku','Female','1995-02-28',2019,'Economics','gracew@gmail.com','0732211455',1),
('Brian','Njoroge','Male','1998-10-12',2022,'Computer Science','bnjoroge@gmail.com','0712345566',3),
('Linda','Chebet','Female','2000-06-05',2023,'Medicine','lchebet@gmail.com','0729988776',4),
('Samuel','Odhiambo','Male','1997-11-30',2021,'Architecture','sodhiambo@gmail.com','0701234432',5),
('Patricia','Nyambura','Female','1999-09-18',2022,'Law','pnyambura@gmail.com','0745566778',6);
SELECT * FROM AlumniDetails;
GO 


INSERT INTO Awards 
(AwardName, AwardYear, AlumniID)
VALUES
('Distinguished Researcher', 2021, 1),
('Outstanding Leadership', 2024, 2),
('Community Impact Award', 2000, 4),
('Innovation in Tech', 2025, 1),
('Entrepreneur of the Year', 2024, 3),
('Excellence in Arts', 2018, 6),
('Rising Star', 2023, 7),
('Innovation in Economics', 2022, 8),
('Best Tech Project', 2024, 9),
('Healthcare Excellence', 2025, 10),
('Design Excellence', 2023, 11),
('Legal Advocacy Award', 2024, 12);
SELECT * FROM Awards;
GO



INSERT INTO Events
(EventID, EventName, EventType, EventDate, Location)
VALUES 
(1,'Annual Gala 2021', 'Social', '2018-10-12', 'Nairobi Main Campus'),
(2,'Tech Symposium', 'Academic', '2022-06-10', 'Engineering Block Hall A'),
(3,'Alumni Homecoming', 'Networking', '2024-08-20', 'University Sports Ground'),
(4,'Career Fair', 'Professional', '2023-09-05', 'Student Center'),
(5,'Health Awareness Walk', 'Charity', '2018-10-12', 'City Park'),
(6,'End of Year Dinner', 'Social', '2025-12-18', 'Safari Park Hotel');
SELECT * FROM Events;
GO


INSERT INTO EventParticipation  
(AlumniID, EventID, Role)
VALUES 
(1, 2, 'Keynote Speaker'),
(2, 1, 'Organizer'),
(3, 3, 'Guest'),
(4, 2, 'Panelist'),
(5, 4, 'Exhibitor'),
(6, 1, 'Volunteer'),
(7, 2, 'Guest Speaker'),
(8, 3, 'Volunteer'),
(9, 2, 'Exhibitor'),
(10, 4, 'Panelist'),
(11, 5, 'Guest'),
(12, 1, 'Organizer');
SELECT * FROM EventParticipation;
GO

INSERT INTO Donations 
(AlumniID, EventID, Amount, DonationDate) 
VALUES 
(1, 1, 5000.00, '2021-05-15'),
(2, 3, 15000.50, '2024-08-20'),
(4, 5, 2500.00, '2018-10-12'),
(6, 1, 10000.00, '2021-05-15'),
(3, 4, 750.00, '2023-09-05'),
(5, 3, 50000.00, '2024-08-20'),
(7, 2, 3000.00, '2023-06-10'),
(8, 3, 4500.00, '2024-08-20'),
(9, 2, 6000.00, '2024-06-10'),
(10, 4, 1200.00, '2023-09-05'),
(11, 5, 8000.00, '2023-10-12'),
(12, 1, 7000.00, '2021-05-15');
SELECT * FROM Donations;
GO


INSERT INTO AlumniPrograms
(ProgramName, ProgramType, StartDate, EndDate, Description)
VALUES 
('Global Mentorship', 'Mentorship', '2015-01-01', '2015-12-31', 'Connecting seniors with alumni.'),
('Graduate Bridge', 'Career', '2025-02-15', '2025-08-15', 'Assisting new grads with job placements.'),
('Research Fellowship', 'Academic', '2026-03-01', '2027-03-01', 'Post-grad research funding.'),
('Alumni Wellness', 'Lifestyle', '2020-04-01', '2020-06-01', 'Mental and physical health seminars.'),
('Startup Incubator', 'Business', '2026-05-20', '2026-11-20', 'Funding for alumni-led startups.'),
('Digital Literacy', 'Education', '2026-07-01', '2026-09-01', 'Community tech training program.');
SELECT *FROM AlumniPrograms;
GO


INSERT INTO ProgramParticipation
(AlumniID, ProgramID, Role) 
VALUES 
(1, 1, 'Senior Mentor'),
(2, 2, 'Career Coach'),
(3, 3, 'Lead Researcher'),
(4, 1, 'Mentee'),
(5, 5, 'Startup Founder'),
(6, 6, 'Tech Instructor'),
(7, 1, 'Mentor'),
(8, 2, 'Participant'),
(9, 3, 'Research Assistant'),
(10, 4, 'Wellness Coach'),
(11, 5, 'Startup Advisor'),
(12, 6, 'Tech Student');
GO
SELECT * FROM ProgramParticipation;
GO

INSERT INTO ExternalInstitutions 
(InstitutionName, Country, City, InstitutionType, Email) 
VALUES 
('Global Tech Corp', 'USA', 'San Francisco', 'Corporate', 'info@globaltech.com'),
('East Africa University', 'Kenya', 'Nairobi', 'Academic', 'registrar@eau.ac.ke'),
('Innovate NGO', 'UK', 'London', 'Non-Profit', 'contact@innovate.org'),
('Smart Systems Ltd', 'Germany', 'Berlin', 'Corporate', 'support@smartsys.de'),
('Regional Research Center', 'Kenya', 'Mombasa', 'Government', 'data@rrc.go.ke'),
('Pan-African Bank', 'South Africa', 'Johannesburg', 'Financial', 'alumni@pabank.com');
GO
SELECT * FROM ExternalInstitutions;
GO


INSERT INTO CollaborationActivities
(InstitutionID, ActivityName, ActivityDate, Description)
VALUES 
(1, 'AI Research Partnership', '2026-04-10', 'Joint study on machine learning.'),
(2, 'Exchange Program', '2025-05-05', 'Student and alumni exchange initiative.'),
(3, 'Sustainable Energy Project', '2024-06-20', 'Building solar labs in rural areas.'),
(5, 'Data Security Seminar', '2026-08-12', 'Training on regional cybersecurity.'),
(4, 'Software Internship Fair', '2023-09-25', 'Recruitment drive for CS alumni.'),
(6, 'Fintech Workshop', '2026-11-02', 'Exploring digital banking trends.');
GO
SELECT * FROM CollaborationActivities;
GO
