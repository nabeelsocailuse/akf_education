import frappe

@frappe.whitelist()
def get_executive_dashboard():
    total_students = frappe.db.count("Student")
    students_in_shilter = frappe.db.count("Program Enrollment", filters={"bed": ["!=", ""]})
    sponsored_childrens = len(frappe.get_all("Sponsorship", filters={"donor_id": ["is", "set"]}, distinct=True, pluck="student_id"))

    return {
        "total_students": total_students,
        "students_in_shilter": students_in_shilter,
        "sponsored_childrens": sponsored_childrens,
        "unsponsored_childrens": (total_students - sponsored_childrens),
        "activity_pictures": student_activity_pictures(),
        "activity_videos": student_activity_videos(),
        "drawing_activity": student_activity_drawing(),
        "student_with_psychological_assessment"
        "charts_data": { 
            "aghosh_homes_interval_count": num_of_aghosh_homes_present(),
            "aghosh_home_status": get_aghosh_home_status(),
            "childens_registration": childens_registration_intervals()
        }
    }

@frappe.whitelist()
def get_aghosh_home_status():
    result = frappe.db.sql("""
        SELECT status, COUNT(status) as total
        FROM `tabAghosh Home`
        WHERE docstatus = 0 AND IFNULL(status, '') != ''
        GROUP BY status
        ORDER BY status
    """, as_dict=True)
    return result

@frappe.whitelist()
def num_of_aghosh_homes_present():
    data = frappe.db.sql("""
        SELECT
            WEEK(Established_Date) AS Week_No,
            COUNT(*) AS Total_Homes
        FROM 
            `tabAghosh Home`
        WHERE 
            MONTH(Established_Date) = MONTH(CURRENT_DATE)  
            AND YEAR(Established_Date) = YEAR(CURRENT_DATE)  
        GROUP BY 
            WEEK(Established_Date)
        ORDER BY 
            WEEK(Established_Date)
    """, as_dict=True)
    return data

@frappe.whitelist()
def childens_registration_intervals():
    data = frappe.db.sql("""
        SELECT
            WEEK(joining_date) AS week_no,
            COUNT(*) AS total_students
        FROM 
            `tabStudent`
        WHERE 
            MONTH(joining_date) = MONTH(CURRENT_DATE)  
            AND YEAR(joining_date) = YEAR(CURRENT_DATE)  
        GROUP BY 
            WEEK(joining_date)
        ORDER BY 
            WEEK(joining_date)
    """, as_dict=True)
    return data

@frappe.whitelist()
def student_activity_pictures():
    data = frappe.db.sql("""
        SELECT 
            COUNT(*) AS total_pictures
        FROM 
            `tabActivity Images` 
        WHERE 
            parenttype = 'Student Activities';
    """, as_dict=True)
    return data

@frappe.whitelist()
def student_activity_videos():
    data = frappe.db.sql("""
        SELECT 
            COUNT(*) AS total_videos
        FROM 
            `tabActivity Videos` 
        WHERE 
            parenttype = 'Student Activities';
    """, as_dict=True)
    return data

@frappe.whitelist()
def student_activity_drawing():
    data = frappe.db.sql("""
        SELECT 
            COUNT(*) AS total_drawings
        FROM 
            `tabChildren Drawings` 
        WHERE 
            parenttype = 'Student Activities';
    """, as_dict=True)
    return data


@frappe.whitelist()
def student_with_psychological_assessment():
    data = frappe.db.sql("""
        SELECT COUNT(s.name) AS student_count
        FROM `tabStudent` s
        JOIN `tabMental Status Examination` mse ON s.name = mse.orphan_name
        WHERE mse.docstatus = 1;
    """, as_dict=True)
    return data
