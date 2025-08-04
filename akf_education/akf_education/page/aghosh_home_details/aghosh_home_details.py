import frappe
@frappe.whitelist()
def get_aghosh_home_dashboard(aghosh_home_id=None):
    sponsored_childrens = frappe.db.sql("""SELECT COUNT(DISTINCT student_id)
                                            FROM `tabSponsorship`
                                            WHERE ifnull(donor_id,"")!="" and aghosh_home_id = %s
                                            AND docstatus = 1
                                        """, (aghosh_home_id,), as_list=True)[0][0] or 0
    # frappe.throw(f"Sponsored Childrens: {sponsored_childrens}")
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
        "probation_staff": probation_staff(aghosh_home_id),
        "intern_staff": intern_staff(aghosh_home_id),
        "staff_distribution_pie": staff_distribution_pie(aghosh_home_id),
        "staff_by_department": staff_by_department(aghosh_home_id),
        "class_wise_summary": class_wise_summary(aghosh_home_id),
        "age_wise_summary": age_wise_summary(aghosh_home_id),
        "donor_wise_summary": donor_wise_summary(aghosh_home_id),
        "sponsorship_breakdown": sponsorship_breakdown(aghosh_home_id),
        "performance": performance(aghosh_home_id),
        "overall_pass_rate": overall_pass_rate(aghosh_home_id),
        "average_score": average_score(aghosh_home_id),
    }

@frappe.whitelist()
def total_students(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "status": "Active"})

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
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "disabled_child": "Yes", "status": "Active"})

@frappe.whitelist()
def children_with_glasses(aghosh_home_id=None):
    return frappe.db.count("Student", filters={"aghosh_home_id": aghosh_home_id, "wear_glasses": "Yes", "status": "Active"})

@frappe.whitelist()
def permanent_staff(aghosh_home_id=None):
    aghosh_branch=frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    return frappe.db.count("Employee", filters={"branch": aghosh_branch,"employment_type": "Confirm"})

@frappe.whitelist()
def contract_staff(aghosh_home_id=None):
    aghosh_branch=frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    return frappe.db.count("Employee", filters={"branch": aghosh_branch,"employment_type": "Contract"})

@frappe.whitelist()
def probation_staff(aghosh_home_id=None):
    aghosh_branch=frappe.db.get_value("Aghosh Home", aghosh_home_id, "branch")
    return frappe.db.count("Employee", filters={"branch": aghosh_branch,"employment_type": "Probation"})

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
            WHEN employment_type = 'Confirm' THEN 'Permanent Staff'
            WHEN employment_type = 'Contract' THEN 'Contractual Staff'
            WHEN employment_type = 'Probation' THEN 'Probation Staff'
            WHEN employment_type = 'Intern' THEN 'Interns'
        END as name,
        COUNT(*) as y,
        CASE 
            WHEN employment_type = 'Confirm' THEN '#f4a261'
            WHEN employment_type = 'Contract' THEN '#f4b261'
            WHEN employment_type = 'Intern' THEN '#f4c261'
            WHEN employment_type = 'Probation' THEN '#f4d261'
        END as color
    FROM `tabEmployee`
    WHERE branch = %s 
      AND employment_type IN ('Confirm', 'Contract', 'Intern', 'Probation')
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
                            WHERE branch = %s
                            GROUP BY department
                            ORDER BY department
                        """, (aghosh_branch,), as_dict=True)
    # employment_type IN ('Confirm', 'Contract', 'Intern')
    
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
                WHERE aghosh_home_id = %s AND status = 'Active'
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

@frappe.whitelist()
def donor_wise_summary(aghosh_home_id=None):
    data = frappe.db.sql(f"""
                            SELECT 
                                donor_type,
                                DATE_FORMAT(creation, '%b %Y') AS month_label,
                                COUNT(*) AS total
                            FROM `tabSponsorship`
                            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                            AND donor_type IN ('Alkhidmat International Network Member', 'Individual Donor', 'Corporate Donor') 
                            AND aghosh_home_id = '{aghosh_home_id}' AND docstatus = 1
                            GROUP BY donor_type, YEAR(creation), MONTH(creation)
                            ORDER BY YEAR(creation), MONTH(creation)
                        """, as_dict=True)
    donor_colors = {
    "Alkhidmat International Network Member": "#1a5df0",
    "Individual Donor": "#f68a0a",
    "Corporate Donor": "#d43f3a"
    }
    
    months = sorted(list({row.month_label for row in data}))
    # frappe.throw(f"months: {months}")

    donor_series = {
    "Individual Donor": [0]*len(months),
    "Corporate Donor": [0]*len(months),
    "Alkhidmat International Network Member": [0]*len(months)
    }

    for row in data:
        month_index = months.index(row.month_label)
        donor_series[row.donor_type][month_index] = row.total

    chart_series = [
        {
            "name": donor_type,
            "data": donor_series[donor_type],
            "color": donor_colors[donor_type]
        }
        for donor_type in donor_series
    ]

    return {
        "categories": months,
        "series": chart_series
    }


@frappe.whitelist()
def sponsorship_breakdown(aghosh_home_id=None):
    # 1️⃣ Count Single/Double/Triple Sponsored students
    single = frappe.db.sql("""
        SELECT COUNT(*) as total FROM (
            SELECT student_id FROM `tabSponsorship`
            WHERE ifnull(donor_id,"")!="" and aghosh_home_id = %s AND docstatus = 1
            GROUP BY student_id HAVING COUNT(*) = 1
        ) t
    """, (aghosh_home_id,),)[0][0]

    double = frappe.db.sql("""
        SELECT COUNT(*) as total FROM (
            SELECT student_id FROM `tabSponsorship`
            WHERE ifnull(donor_id,"")!="" and aghosh_home_id = %s AND docstatus = 1
            GROUP BY student_id HAVING COUNT(*) = 2
        ) t
    """, (aghosh_home_id,),)[0][0]

    triple = frappe.db.sql("""
        SELECT COUNT(*) as total FROM (
            SELECT student_id FROM `tabSponsorship`
            WHERE ifnull(donor_id,"")!="" and aghosh_home_id = %s AND docstatus = 1
            GROUP BY student_id HAVING COUNT(*) = 3
        ) t
    """, (aghosh_home_id,),)[0][0]

    # 2️⃣ Count Sponsorship by Type
    head_office = frappe.db.count("Sponsorship", {"sponsorship_type": "Head Office", "aghosh_home_id": aghosh_home_id, "docstatus": 1})
    local = frappe.db.count("Sponsorship", {"sponsorship_type": "Local Sponsored", "aghosh_home_id": aghosh_home_id, "docstatus": 1})
    regional = frappe.db.count("Sponsorship", {"sponsorship_type": "Regional Sponsored", "aghosh_home_id": aghosh_home_id, "docstatus": 1})

    # 3️⃣ Combine for Chart
    result = [{
        "name": "Sponsorship Type",
        "data": [single, double, triple, head_office, local, regional],
        "color": "#f39c12"
    }]
    # frappe.throw(f"result: {result[0]['data'][0]}")
    return result

@frappe.whitelist()
def performance(aghosh_home_id=None):
    data = frappe.db.sql("""
                            SELECT 
                                academic_year,
                                SUM(CASE WHEN total_percentage BETWEEN 40 AND 60 THEN 1 ELSE 0 END) AS range_40_60,
                                SUM(CASE WHEN total_percentage BETWEEN 61 AND 80 THEN 1 ELSE 0 END) AS range_61_80,
                                SUM(CASE WHEN total_percentage BETWEEN 81 AND 100 THEN 1 ELSE 0 END) AS range_81_100
                            FROM `tabAssessment Result`
                            WHERE select_term = 'Final Term' AND docstatus = 1 AND aghosh_home_id = %s
                            GROUP BY academic_year
                            ORDER BY academic_year DESC
                            LIMIT 5
                        """, (aghosh_home_id,), as_dict=True)

    # Reverse to show oldest first
    data = list(reversed(data))

    categories = [row.academic_year for row in data]
    range_40_60 = [row.range_40_60 for row in data]
    range_61_80 = [row.range_61_80 for row in data]
    range_81_100 = [row.range_81_100 for row in data]

    result = [
        { "name": "40% - 60%", "data": range_40_60, "color": "#007bff" },
        { "name": "61% - 80%", "data": range_61_80, "color": "#28a745" },
        { "name": "81% - 100%", "data": range_81_100, "color": "#9b59b6" }
    ]
    return { "categories": categories, "series": result }

@frappe.whitelist()
def overall_pass_rate(aghosh_home_id=None):
    data = frappe.db.sql("""
                            SELECT 
                                academic_year,
                                COUNT(*) AS total_students,
                                SUM(CASE WHEN total_percentage >= 40 THEN 1 ELSE 0 END) AS passed_students
                            FROM `tabAssessment Result`
                            WHERE select_term = 'Final Term' and docstatus = 1 AND aghosh_home_id = %s
                            GROUP BY academic_year
                            ORDER BY academic_year DESC
                            LIMIT 5
                        """, (aghosh_home_id,), as_dict=True)

    data = list(reversed(data))

    # categories = [row.academic_year for row in data]
    overall_pass_rate = [
        round((row.passed_students / row.total_students) * 100, 2) if row.total_students else 0
        for row in data
    ]
    # frappe.throw(f"pass_rate: {pass_rate}")
    return overall_pass_rate

@frappe.whitelist()
def average_score(aghosh_home_id=None):
    data = frappe.db.sql("""
                            SELECT 
                                academic_year,
                                ROUND(AVG(total_percentage), 2) AS avg_score
                            FROM `tabAssessment Result`
                            WHERE select_term = 'Final Term' AND docstatus = 1 AND aghosh_home_id = %s
                            GROUP BY academic_year
                            ORDER BY academic_year DESC
                            LIMIT 5
                        """, (aghosh_home_id,), as_dict=True)

    data = list(reversed(data))

    # categories = [row.academic_year for row in data]
    average_score = [round(row.avg_score, 2) if row.avg_score is not None else 0 for row in data]
    # frappe.throw(f"avg_score: {avg_score}")
    return average_score