import frappe

@frappe.whitelist()
def get_executive_dashboard():
    total_students = frappe.db.count("Student")
    students_in_shilter = frappe.db.count("Program Enrollment", filters={"bed": ["!=", ""]})
    sponsored_childrens = frappe.db.sql("""SELECT COUNT(DISTINCT student_id)
                FROM `tabSponsorship`
                WHERE ifnull(donor_id,"")!="";
                """)[0][0] or 0

    return {
        "total_students": total_students,
        "students_in_shilter": students_in_shilter,
        "sponsored_childrens": sponsored_childrens,
        "unsponsored_childrens": (total_students - sponsored_childrens),
        # "activity_pictures": student_activity_pictures(),
        # "activity_videos": student_activity_videos(),
        "drawing_activity": student_activity_drawing(),
        "student_with_psychological_assessment": student_with_psychological_assessment(),
        "charts_data": {
            "aghosh_homes_interval_count": num_of_aghosh_homes_present(),
            "aghosh_home_status": get_aghosh_home_status(),
            "childens_registration": childens_registration_intervals(),
        },
        "aghosh_home_locations": get_aghosh_home_locations()  
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
            YEAR(Established_Date) AS Year, 
            COUNT(*) AS aghosh_home
        FROM 
            `tabAghosh Home`
        WHERE
            Established_Date IS NOT NULL
        GROUP BY 
            YEAR(Established_Date)
        ORDER BY 
            YEAR(Established_Date) ASC;
    """, as_dict=True)
    return data


@frappe.whitelist()
def childens_registration_intervals():
    data = frappe.db.sql("""
        SELECT
            YEAR(joining_date) AS Year,
            COUNT(*) AS student_count
        FROM
            `tabStudent`
        WHERE
            joining_date IS NOT NULL
        GROUP BY
            YEAR(joining_date)
        ORDER BY
            YEAR(joining_date) ASC;
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
        JOIN `tabMental Status Examination` mse ON s.name = mse.student_name
        WHERE mse.docstatus = 1;
    """, as_dict=True)
    return data

@frappe.whitelist()
def get_aghosh_home_locations():
    data = frappe.db.sql("""
        SELECT aghosh_home_name, longitude, latitude, status
        FROM `tabAghosh Home`
        WHERE longitude IS NOT NULL AND latitude IS NOT NULL 
          AND longitude != '' AND latitude != ''
    """, as_dict=True)

    locations = []
    for record in data:
        if record["latitude"] and record["longitude"]:
            locations.append({
                "coords": [float(record["latitude"]), float(record["longitude"])],
                "name": record["aghosh_home_name"],
                "status": record["status"]
            })

    return locations



