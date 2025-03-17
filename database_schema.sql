CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(50),
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin'))
);

CREATE TABLE students (
    user_id INT PRIMARY KEY,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    face_embedding TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE staff (
    user_id INT PRIMARY KEY,
    employee_number VARCHAR(20) NOT NULL UNIQUE,
    position VARCHAR(20) CHECK (position IN ('teacher', 'administrator')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    academic_year SMALLINT NOT NULL,
    semester VARCHAR(10) CHECK (semester IN ('spring', 'fall'))
);

CREATE TABLE attendance_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    release_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP NOT NULL,
    auth_method VARCHAR(20) CHECK (auth_method IN ('face', 'location', 'code')),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE attendance_records (
    record_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('present', 'absent', 'late')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(user_id),
    FOREIGN KEY (event_id) REFERENCES attendance_events(event_id)
);

CREATE TABLE course_participants (
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    role VARCHAR(10) CHECK (role IN ('student', 'teacher')),
    enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);