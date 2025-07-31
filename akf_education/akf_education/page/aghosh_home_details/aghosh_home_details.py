import frappe
@frappe.whitelist()
def get_aghosh_home_dashboard(aghosh_home_id=None):
    sponsored_childrens = frappe.db.sql("""SELECT COUNT(DISTINCT student_id)
                                            FROM `tabSponsorship`
                                            WHERE ifnull(donor_id,"")!="" and aghosh_home_id = %s
                                            AND docstatus = 1
                                        """, (aghosh_home_id,), as_list=True)[0][0] or 0
    return {
        "aghosh_home_name": frappe.db.get_value("Aghosh Home", aghosh_home_id, "aghosh_home_name") if aghosh_home_id else None,
        "total_students": total_students(aghosh_home_id),
        "total_beds": total_beds(aghosh_home_id),
        "total_rooms": total_rooms(aghosh_home_id),
        "sponsored_childrens": sponsored_childrens,
        "total_cameras": total_cameras(aghosh_home_id),
        "active_cameras": active_cameras(aghosh_home_id),
        "inactive_cameras": inactive_cameras(aghosh_home_id),
        "disabled_students": disabled_students(aghosh_home_id),
        "children_with_glasses": children_with_glasses(aghosh_home_id),
        "permanent_staff": permanent_staff(aghosh_home_id),
        "contract_staff": contract_staff(aghosh_home_id),
        "intern_staff": intern_staff(aghosh_home_id),
        "staff_distribution_pie": staff_distribution_pie(aghosh_home_id),
        "staff_by_department": staff_by_department(aghosh_home_id),
        "class_wise_summary": class_wise_summary(aghosh_home_id),
        "age_wise_summary": age_wise_summary(aghosh_home_id)
    }

@frappe.whitelist()
def total_students(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id})

@frappe.whitelist()
def total_beds(aghosh_home_id=None):
    return frappe.db.count("Beds", filters={"aghosh_home_id": aghosh_home_id})

@frappe.whitelist()
def total_rooms(aghosh_home_id=None):
    return frappe.db.count("Rooms", filters={"aghosh_home_id": aghosh_home_id})

@frappe.whitelist()
def total_cameras(aghosh_home_id=None):
    return frappe.db.get_value("Aghosh Home", aghosh_home_id, "total_cameras") or 0

@frappe.whitelist()
def active_cameras(aghosh_home_id=None):
    return frappe.db.get_value("Aghosh Home", aghosh_home_id, "active_camera_count") or 0

@frappe.whitelist()
def inactive_cameras(aghosh_home_id=None):
    return frappe.db.get_value("Aghosh Home", aghosh_home_id, "inactive_camera_count") or 0

@frappe.whitelist()
def disabled_students(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "disabled_child": "Yes"})

@frappe.whitelist()
def children_with_glasses(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "wear_glasses": "Yes"})

@frappe.whitelist()
def permanent_staff(aghosh_home_id=None):
    aghosh_branch=frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    return frappe.db.count("Employee", filters={"branch": aghosh_branch,"employment_type": "Permanent"})

@frappe.whitelist()
def contract_staff(aghosh_home_id=None):
    aghosh_branch=frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    return frappe.db.count("Employee", filters={"branch": aghosh_branch,"employment_type": "Contract"})

@frappe.whitelist()
def intern_staff(aghosh_home_id=None):
    aghosh_branch=frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    return frappe.db.count("Employee", filters={"branch": aghosh_branch,"employment_type": "Intern"})

####        Staff Distribution Pie Chart Data        ####
# Note: The pie chart data is expected to be in the format:
                    # { name: 'Permanent Staff', y: 28, color: '#f4a261' },
					# { name: 'Contractual Staff', y: 12, color: '#f4b261' },
					# { name: 'Interns', y: 5, color: '#f4c261' }
@frappe.whitelist()
def staff_distribution_pie(aghosh_home_id=None):
    aghosh_branch = frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    data = frappe.db.sql("""
    SELECT
        CASE 
            WHEN employment_type = 'Permanent' THEN 'Permanent Staff'
            WHEN employment_type = 'Contract' THEN 'Contractual Staff'
            WHEN employment_type = 'Intern' THEN 'Interns'
        END as name,
        COUNT(*) as y,
        CASE 
            WHEN employment_type = 'Permanent' THEN '#f4a261'
            WHEN employment_type = 'Contract' THEN '#f4b261'
            WHEN employment_type = 'Intern' THEN '#f4c261'
        END as color
    FROM `tabEmployee`
    WHERE branch = %s 
      AND employment_type IN ('Permanent', 'Contract', 'Intern')
    GROUP BY employment_type
""", (aghosh_branch,), as_dict=True)
    
    return data

@frappe.whitelist()
def staff_by_department(aghosh_home_id=None):
    aghosh_branch = frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    data = frappe.db.sql("""
                            SELECT
                                department,
                                COUNT(*) as count
                            FROM `tabEmployee`
                            WHERE branch = %s AND employment_type IN ('Permanent', 'Contract', 'Intern')
                            GROUP BY department
                            ORDER BY department
                        """, (aghosh_branch,), as_dict=True)
    
    categories = [row.department or "Not Assigned" for row in data]
    counts = [row.count for row in data]
    # result = {"categories": categories, "counts": counts}
    # frappe.throw(f"result: {result['categories']}")

    return {
        "categories": categories,
        "counts": counts
    }


@frappe.whitelist()
def class_wise_summary(aghosh_home_id=None):
    data = frappe.db.sql("""
                SELECT 
                    CASE
                        WHEN program LIKE 'Class 1' OR program LIKE 'Class 2' OR program LIKE 'Class 3' THEN 'Class 1-3'
                        WHEN program LIKE 'Class 4' OR program LIKE 'Class 5' OR program LIKE 'Class 6' THEN 'Class 4-6'
                        WHEN program LIKE 'Class 7' OR program LIKE 'Class 8' OR program LIKE 'Class 9' THEN 'Class 7-9'
                        WHEN program LIKE 'Class 10' OR program LIKE 'Class 11' OR program LIKE 'Class 12' THEN 'Class 10-12'
                    END as class_group,
                    COUNT(*) as y
                FROM `tabProgram Enrollment`
                WHERE aghosh_home_id = %s AND active = 1
                GROUP BY class_group
            """, (aghosh_home_id,), as_dict=True)
    
    return data

@frappe.whitelist()
def age_wise_summary(aghosh_home_id=None):
    data = frappe.db.sql("""
                SELECT 
                    CASE
                        WHEN age BETWEEN 5 AND 8 THEN '5-8 years'
                        WHEN age BETWEEN 9 AND 12 THEN '9-12 years'
                        WHEN age BETWEEN 13 AND 16 THEN '13-16 years'
                        WHEN age BETWEEN 17 AND 20 THEN '17-20 years'
                    END as age_group,
                    COUNT(*) as y
                FROM `tabStudent`
                WHERE aghosh_home_id = %s
                GROUP BY age_group
                ORDeR BY age_group         
            """, (aghosh_home_id,), as_dict=True)

    categories = [row.age_group or "Not Assigned" for row in data]
    y = [row.y for row in data]
    # result = {"categories": categories, "counts": counts}
    # frappe.throw(f"result: {result['categories']}")

    return {
        "categories": categories,
        "y": y
    }