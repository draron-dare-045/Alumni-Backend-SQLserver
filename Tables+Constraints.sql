USE Alumnidb;
--Tables And Constraints
CREATE TABLE AlumniDetails (
    AlumniID INT PRIMARY KEY IDENTITY(1,1),
    RegistrationNumber VARCHAR(50) UNIQUE NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Gender VARCHAR(10),
    DateOfBirth DATE,
    GraduationYear INT,
    Degree VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    ChapterID INT,

    IsVerified BIT DEFAULT 0,
);

CREATE TABLE Awards (
    AwardID INT PRIMARY KEY IDENTITY(1,1),
    AwardName VARCHAR(100),
    AwardYear INT,
    AlumniID INT,
    FOREIGN KEY (AlumniID) REFERENCES AlumniDetails(AlumniID)
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY IDENTITY(1,1),
    EventName VARCHAR(100),
    EventType VARCHAR(50),
    EventDate DATE,
    Location VARCHAR(100)
);

CREATE TABLE EventParticipation (
    ParticipationID INT PRIMARY KEY IDENTITY(1,1),
    AlumniID INT,
    EventID INT,
    Role VARCHAR(50),
    FOREIGN KEY (AlumniID) REFERENCES AlumniDetails(AlumniID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE Donations (
    DonationID INT PRIMARY KEY IDENTITY(1,1),
    AlumniID INT,
    EventID INT,
    Amount DECIMAL(10,2),
    DonationDate DATE,
    FOREIGN KEY (AlumniID) REFERENCES AlumniDetails(AlumniID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);

CREATE TABLE AlumniPrograms (
    ProgramID INT PRIMARY KEY IDENTITY(1,1),
    ProgramName VARCHAR(100),
    ProgramType VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Description TEXT
);

CREATE TABLE ProgramParticipation (
    ParticipationID INT PRIMARY KEY IDENTITY(1,1),
    AlumniID INT,
    ProgramID INT,
    Role VARCHAR(50),
    FOREIGN KEY (AlumniID) REFERENCES AlumniDetails(AlumniID),
    FOREIGN KEY (ProgramID) REFERENCES AlumniPrograms(ProgramID)
);

CREATE TABLE ExternalInstitutions (
    InstitutionID INT PRIMARY KEY IDENTITY(1,1),
    InstitutionName VARCHAR(100),
    Country VARCHAR(50),
    City VARCHAR(50),
    InstitutionType VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE CollaborationActivities (
    CollaborationID INT PRIMARY KEY IDENTITY(1,1),
    InstitutionID INT,
    ActivityName VARCHAR(100),
    ActivityDate DATE,
    Description TEXT,
    FOREIGN KEY (InstitutionID) REFERENCES ExternalInstitutions(InstitutionID)
);