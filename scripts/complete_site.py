"""Build the missing static screens and shared components for the content migration.
Run from the repository root: python3 scripts/complete_site.py.
Existing screenshot-based page bodies are preserved except where incomplete content is replaced.
"""
from pathlib import Path
import re, json, html
ROOT=Path(__file__).resolve().parents[1]
def esc(s): return html.escape(str(s),quote=True)
def link(url,label):return f'<a href="{esc(url)}">{esc(label)}</a>'
def p(s):return '<p>'+s+'</p>'
def ul(items):return '<ul>'+''.join('<li>'+x+'</li>' for x in items)+'</ul>'
def button(url,label):return f'<a class="btn btn--primary" href="{esc(url)}">{esc(label)}</a>'
def actions(items):return '<div class="action-row">'+''.join(button(u,t) for u,t in items)+'</div>'
def note(s,urgent=False):return '<div class="info-panel'+(' info-panel--urgent' if urgent else '')+'">'+p(s)+'</div>'
def cards(items):return '<div class="directory-grid">'+''.join(f'<a class="directory-card" href="{esc(u)}"><h3>{esc(t)}</h3><p>{esc(d)}</p><span>Explore {esc(t.lower())} →</span></a>' for u,t,d in items)+'</div>'
def resources(items):return '<ul class="resource-list">'+''.join('<li>'+link(u,t)+'</li>' for u,t in items)+'</ul>'
APPLY='https://applyindia.uwa.edu.au/uwa-india-application-form'
INDIA='https://india.uwa.edu.au/'
ENGLISH='https://www.uwa.edu.au/study/how-to-apply/pathways-and-eligibility/english-language-requirements'
MHA='https://www.mha.gov.in/emergency-response-support-system-erss'
CONTACT_EMAIL='info.uwaindia@uwa.edu.au'
CONTACT_PHONE='+917943447630'
COURSES=[
 {'slug':'computer-science','name':'Bachelor of Science (Computer Science)','level':'Undergraduate','campuses':['Mumbai','Chennai'],'duration':'3 years','area':'Computing','overview':'Develop knowledge and skills in computer science, programming and the design of computing solutions.','domestic':'14,52,200','international':'16,69,800'},
 {'slug':'data-science','name':'Bachelor of Science (Data Science)','level':'Undergraduate','campuses':['Mumbai','Chennai'],'duration':'3 years','area':'Data','overview':'Explore the analysis and interpretation of data, building skills for data-driven problem solving.','domestic':'14,52,200','international':'16,69,800'},
 {'slug':'cybersecurity','name':'Bachelor of Science (Cybersecurity)','level':'Undergraduate','campuses':['Mumbai'],'duration':'3 years','area':'Computing','overview':'Develop your understanding of cybersecurity and the protection of digital systems and information.','domestic':'14,52,200','international':'16,69,800'},
 {'slug':'artificial-intelligence-extended-major','name':'Bachelor of Advanced Computer Science — Artificial Intelligence','level':'Undergraduate','campuses':['Mumbai','Chennai'],'duration':'4 years','area':'Computing','overview':'Study advanced computing and artificial intelligence, developing skills for intelligent computational systems.','domestic':'17,93,000','international':'20,61,950'},
 {'slug':'business-management','name':'Bachelor of Business (Business Management)','level':'Undergraduate','campuses':['Mumbai','Chennai'],'duration':'3 years','area':'Business','overview':'Build a foundation in business and management, preparing to understand organisations and their operations.','domestic':'14,52,200','international':'16,69,800'},
 {'slug':'global-business','name':'Bachelor of Business (Global Business)','level':'Undergraduate','campuses':['Mumbai'],'duration':'3 years','area':'Business','overview':'Explore business in an international context and the opportunities and challenges of operating across borders.','domestic':'14,52,200','international':'16,69,800'},
 {'slug':'enterprise-and-innovation','name':'Bachelor of Business (Enterprise and Innovation)','level':'Undergraduate','campuses':['Mumbai'],'duration':'3 years','area':'Business','overview':'Develop your understanding of enterprise and innovation, including the creation and growth of new business ideas.','domestic':'14,52,200','international':'16,69,800'},
 {'slug':'master-of-information-technology','name':'Master of Information Technology','level':'Postgraduate','campuses':['Mumbai','Chennai'],'duration':'2 years','area':'Computing','overview':'Build expertise in software development, data, artificial intelligence and computing systems.','domestic':'19,25,000','international':'22,13,750'},
 {'slug':'master-of-business-administration','name':'Master of Business Administration','level':'Postgraduate','campuses':['Mumbai','Chennai'],'duration':'1 year (accelerated)','area':'Business','overview':'Advance your understanding of business functions, management and organisational decision-making.','domestic':'23,10,000','international':'26,56,500'},
]
for c in COURSES:c['url']='course-'+c['slug']+'.html';c['source']=INDIA+'courses/'+c['slug']
(ROOT/'assets/data/courses.json').write_text(json.dumps(COURSES,indent=2)+'\n')
FAQS=[
 ('How do I choose a course?','Explore our '+link('undergraduate-courses.html','undergraduate')+' and '+link('postgraduate-courses.html','postgraduate')+' courses. Make a note of your preferred course and intake, and contact an advisor if you need guidance.'),
 ('What entry requirements do I need to meet?','Check the academic and English language entry requirements for your chosen course. Requirements can vary by course and level of study. See '+link('english-language-requirements.html','English language requirements')+' and the official course information.'),
 ('What documents will I need?','Prepare academic transcripts and certificates, English language test results if required, a copy of your passport, and any additional documents specified for your course, such as a CV or portfolio.'),
 ('How can I apply?','Apply directly online to UWA India or through an authorised UWA India education agent. Follow the '+link('how-to-apply.html','application guide')+' for the five steps.'),
 ('What happens after I submit an application?','Your application will be assessed against your chosen course’s entry requirements. If successful, you will receive a conditional or unconditional offer and an offer letter outlining your next steps.'),
 ('Where can I find fee and scholarship information?','See '+link('fees.html','Fees')+' and '+link('scholarships.html','Scholarships')+'. Check the current official course and scholarship information before applying.'),
 ('How do I get academic or library support?','Visit '+link('academic-support.html','Academic support')+' or the '+link('library.html','Library')+' for learning, information and referencing support.'),
 ('Where can I find my unit materials and recordings?','Your unit information, learning materials, recordings and assessments are available through the '+link('lms.html','Blackboard Ultra LMS')+'. Sign in using your UWA account.'),
]
def faq_module(limit=None):return '<div class="faq-list" data-rendering="FAQs">'+''.join('<details><summary>'+esc(q)+'</summary>'+p(a)+'</details>' for q,a in FAQS[:limit])+'</div>'
def enquiry(prefix='enquiry'):
 return f'''<section class="enquiry-module" id="{prefix}" aria-labelledby="{prefix}-title" data-rendering="EnquiryForm">
 <h2 id="{prefix}-title">Let’s connect</h2><p>Tell our team what you would like to know about studying at UWA India. This form prepares an email enquiry for you to send.</p>
 <form data-enquiry-form>
 <div class="enquiry-grid">
 <div><label for="{prefix}-name">Your name (required)</label><input id="{prefix}-name" name="name" autocomplete="name" required maxlength="120"></div>
 <div><label for="{prefix}-email">Email address (required)</label><input id="{prefix}-email" name="email" type="email" autocomplete="email" required maxlength="254"></div>
 <div><label for="{prefix}-phone">Phone number</label><input id="{prefix}-phone" name="phone" type="tel" autocomplete="tel" maxlength="30"></div>
 <div><label for="{prefix}-campus">Preferred campus</label><select id="{prefix}-campus" name="campus"><option value="">Please select</option><option>Mumbai</option><option>Chennai</option><option>Not sure yet</option></select></div>
 <div class="full-field"><label for="{prefix}-course">Course or enquiry topic</label><select id="{prefix}-course" name="topic"><option>General enquiry</option>{''.join('<option>'+esc(c['name'])+'</option>' for c in COURSES)}<option>Fees and scholarships</option><option>Student support</option></select></div>
 <div class="full-field"><label for="{prefix}-message">Your message (required)</label><textarea id="{prefix}-message" name="message" required maxlength="4000" rows="5"></textarea></div>
 </div><label class="enquiry-consent"><input type="checkbox" required name="consent"><span>I agree to include these details in an email enquiry to UWA India. I have read the <a href="https://www.uwa.edu.au/privacy">privacy information</a>.</span></label>
 <button class="btn btn--primary" type="submit">Prepare email enquiry</button>
 <p class="form-status" role="status" aria-live="polite"></p>
 <a class="enquiry-fallback" href="mailto:{CONTACT_EMAIL}">Email {CONTACT_EMAIL} directly</a>
 <noscript><p>You can email our team directly using the link above.</p></noscript>
 </form></section>'''
def contact_module():return '<section class="contact-module container" aria-labelledby="shared-contact-title" data-rendering="ContactUs"><h2 id="shared-contact-title">Talk to UWA India</h2><p>Speak to our team for guidance on courses, applications and studying at UWA India.</p>'+actions([('contact.html','Contact us'),('faqs.html','View FAQs')])+'</section>'
# Reuse the complete branded header/footer artwork from the existing Study screen.
HEAD=(ROOT/'scripts/templates/header.html').read_text()
FOOTER=(ROOT/'scripts/templates/footer.html').read_text()
PAGES=[]
def section(id,title,body):return {'id':id,'title':title,'body':body}
def add(slug,title,group,lead,sections,photo=None,source=None,form=False):
 PAGES.append({'slug':slug,'title':title,'group':group,'lead':lead,'sections':sections,'photo':photo,'source':source,'form':form})
add('student-life','Student life','Student life','A vibrant university experience starts here.',[
 section('community','A community beyond the classroom',p("At UWA India, university life extends beyond the classroom. Alongside a world-class education, you'll have opportunities to connect with a diverse community, explore new interests, develop valuable skills and create lasting friendships.")+p("Whether you're focused on academic success, personal growth or preparing for your future career, our campus will offer a range of experiences designed to help you make the most of your time at university.")),
 section('experiences','Make the most of university life',p('At UWA India, you can look forward to:')+ul(['Clubs and societies spanning a wide range of interests','Hackathons, innovation challenges and entrepreneurial competitions','Cultural celebrations and community events','Guest lectures, debates, panel discussions and industry forums','Leadership development programmes and volunteering opportunities','Networking events and opportunities to engage with industry professionals','Health, wellbeing and recreational activities that support a balanced student experience'])+p("At UWA India, you'll be part of a dynamic and inclusive community that encourages curiosity, collaboration and lifelong connections.")),
 section('explore','Explore student life',cards([('events.html','Events','Find official event listings and opportunities to connect.'),('student-support-services.html','Student support services','Find academic, library and wellbeing support.'),('campus-facilities.html','Campus facilities','Discover our Mumbai and Chennai campuses.'),('safety-on-campus.html','Safety on campus','Find emergency guidance and support contacts.')]))
],photo='career-students.jpg',source='PDF pages 8–9')
add('events','Events','Student life','Connect with UWA India through events, information sessions and community activities.',[
 section('listings','Official event listings',p('Check the official listings for event dates, locations, registration and availability before planning your visit.')+cards([(INDIA+'upcoming-events','Upcoming events','View the current event information published by UWA India.'),(INDIA+'whats-new','What’s new','Explore news, information sessions and campus updates.')])+p('For help with an event or a campus visit, '+link('contact.html','contact our team')+'.')),
 section('local-events','Find an event','<form data-event-filter><label for="event-campus">Campus</label><select class="filter-control" id="event-campus"><option value="all">All campuses</option><option value="Mumbai">Mumbai</option><option value="Chennai">Chennai</option></select></form><p id="event-status" role="status">2 campus event directories</p><div class="directory-grid"><a class="directory-card" data-event-campus="Mumbai" href="https://india.uwa.edu.au/upcoming-events"><h3>Mumbai campus event information</h3><p>Check the published session information and confirm dates and registration before your visit.</p><span>View official event information →</span></a><a class="directory-card" data-event-campus="Chennai" href="https://india.uwa.edu.au/whats-new"><h3>Chennai campus event information</h3><p>Check the published session information and confirm dates and registration before your visit.</p><span>View official event information →</span></a></div>')
],source='PDF page 9; official UWA India event directories')
add('safety-on-campus','Safety on campus','Student life','Know where to find help in Mumbai and Chennai.',[
 section('emergency','In an emergency',note('For an immediate emergency in India, call '+link('tel:112','112')+'. The national emergency service connects callers with police, fire, health and other emergency assistance.',True)+p('If it is safe to do so, move away from immediate danger and follow the instructions of emergency responders.')+p(link(MHA,'Government of India emergency service information'))),
 section('campus-security','Campus security and emergency procedures',p('Follow the safety information and emergency instructions provided at your campus. Locate your nearest exits and assembly information when you arrive.')+p('Contact the UWA India team for current campus-specific security contacts, assembly points and after-hours arrangements. For an immediate emergency in India, call 112.')+actions([('contact.html','Ask about campus safety'),('campus-facilities.html','Campus information')])),
 section('wellbeing','Wellbeing and non-urgent support',p('For non-urgent student wellbeing support during operating hours, email '+link('mailto:student-wellbeing@india.uwa.edu.au','student-wellbeing@india.uwa.edu.au')+'. This email is not an emergency service.')+p('If you need urgent help outside operating hours, call '+link('tel:112','112')+' for an emergency in India.')+p(link(INDIA+'current-students/wellbeing-support/wellbeing-services','Official UWA India wellbeing services'))),
 section('personal-safety','Arriving in Mumbai or Chennai',ul(['Plan your route to campus and keep the campus address available.','Keep your phone charged and save important contact details.','Ask campus staff about local arrival, building access and safety arrangements.','Report safety concerns to campus staff; call 112 if there is an immediate emergency.']))
],source='PDF page 9 (campus-specific content awaiting confirmation); MHA ERSS and official UWA India wellbeing page')
add('student-support-services','Student support services','Student life','Find support for learning, library resources, wellbeing and your university experience.',[
 section('library-support','Library and learning resources',p('Students enrolled at UWA India gain access to the UWA University Library’s online ebook and journal collections. Access your unit’s essential textbook and search high quality scholarly sources relevant to the courses taught at UWA India. Expert Library and Learning Resource Advisors on campus at Mumbai and Chennai can guide students in how to best use these Library resources, and provide support with other study skills.')+button('library.html','Explore the Library')),
 section('support-options','Find the right support',cards([('academic-support.html','Academic support','Get help with writing, study skills and academic integrity.'),('lms.html','Learning Management System','Find unit materials, recordings, grades and feedback.'),('career-support.html','Career support','Explore resources for career preparation and employability.'),('safety-on-campus.html','Wellbeing and safety','Find wellbeing contacts and emergency guidance.')]))
],source='PDF page 9; linked support sections from pages 10–16')
MUMBAI='2nd Floor, Waterstones, Marol, Andheri East, Off International Airport (Sahar) Road, Mumbai 400059, Maharashtra.'
CHENNAI='7th Floor, One National Park, Old Door 66/New Door 142, Velachery Road, Velachery, Chennai 600042, Tamil Nadu.'
mumbai_body=p("Located in Andheri, one of Mumbai's key commercial and education hubs, the UWA India Mumbai campus sits at the heart of a vibrant business ecosystem. With close proximity to major corporate offices, start-ups and strong transport connectivity, students are immersed in a dynamic professional environment from day one.")+ul(['Tech-enabled classrooms and lecture theatres','Innovation and project laboratories','Group work and collaboration studios','Student hub and social spaces','High-speed internet and digital infrastructure throughout'])
chennai_body=p('Located on Velachery Road within Chennai’s dynamic technology and business hub, UWA India offers students unparalleled access to industry, employers and professional networks, enabling them to build valuable connections while earning a globally recognised degree close to home.')+ul(['Modern teaching and learning spaces','Technology and computing labs','Student collaboration zones',"Close proximity to Chennai's IT and business districts"])
mumbai_travel=p('The content document describes the campus as five minutes from the airport, a one-minute walk to Marol Naka Metro station, 3 km from the Western Express Highway and 5.7 km from the Eastern Express Highway. Travel time depends on your route and traffic.')
def directions(address):return 'https://www.google.com/maps/search/?api=1&query='+__import__('urllib.parse',fromlist=['quote']).quote(address)
add('campus-facilities','Campus facilities','Student life','Discover modern learning environments in Mumbai and Chennai.',[
 section('mumbai','Mumbai Campus, Andheri',mumbai_body+p(MUMBAI)+mumbai_travel+actions([('campus-mumbai.html','Explore Mumbai campus'),(directions(MUMBAI),'Open Mumbai map')])),
 section('chennai','Chennai Campus, Velachery',chennai_body+p(CHENNAI)+actions([('campus-chennai.html','Explore Chennai campus'),(directions(CHENNAI),'Open Chennai map')])),
 section('campus-libraries','Campus libraries',p('The Mumbai and Chennai campus libraries provide quiet spaces for individual study. Bring Your Own Device stations let you connect your own device to a monitor using USB-C.')+button('library.html','Library spaces and services'))
],photo='join-uwa.jpg',source='PDF pages 9–10 and 14; addresses from official UWA India contact page')
add('campus-mumbai','Mumbai campus','Student life','Study in Andheri, close to Mumbai’s business and innovation networks.',[
 section('facilities','Campus facilities',mumbai_body),section('getting-here','Getting here',p(MUMBAI)+mumbai_travel+button(directions(MUMBAI),'Open campus map')),
 section('support','Support at your campus',cards([('library.html','Library','Access collections, study spaces and learning advice.'),('student-support-services.html','Student support','Find support and services for your studies.')]))
],photo='campus-mumbai.jpg',source='PDF pages 9–10; official UWA India contact page')
add('campus-chennai','Chennai campus','Student life','Study on Velachery Road in Chennai’s technology and business hub.',[
 section('facilities','Campus facilities',chennai_body),section('getting-here','Getting here',p(CHENNAI)+button(directions(CHENNAI),'Open campus map')),
 section('support','Support at your campus',cards([('library.html','Library','Access collections, study spaces and learning advice.'),('student-support-services.html','Student support','Find support and services for your studies.')]))
],photo='campus-chennai.jpg',source='PDF pages 9–10; official UWA India contact page')
add('current-students','Current students','Current students','Your starting point for learning resources, support and life at UWA India.',[
 section('learning','Learning and study',cards([('academic-support.html','Academic support','Writing, study skills, integrity and individual support.'),('library.html','Library','Online collections, referencing and campus study spaces.'),('lms.html','LMS','Access Blackboard Ultra, unit materials and grades.'),('career-support.html','Career support','Prepare for your future career.')])),
 section('student-life','Support and campus life',cards([('student-support-services.html','Student support services','Find the right team for your enquiry.'),('events.html','Events','Explore official event listings.'),('campus-facilities.html','Campus facilities','Find campus information and maps.'),('safety-on-campus.html','Safety and wellbeing','Know where to find help.')]))
],source='PDF pages 10–16')
add('academic-support','Academic support','Current students','Get advice and resources to support your study success.',[
 section('learning-support','Your Learning Support Coordinator',p('You can access free advice, workshops, resources, and support for your study success from our dedicated Learning Support Coordinator. Get help to improve your study techniques, time management, writing, English language, research skills and more.')),
 section('academic-writing','Academic Writing',p('Your Learning Support Coordinator can support you with how to structure academic documents, improve grammar and write with a professional academic tone.')),
 section('study-skills','Study Skills',p('Time management, note taking and preparing for exams and tests are important skills for university students. Access the online resources or speak to your Learning Support Coordinator for support with any of these study skills.')),
 section('academic-integrity','Academic Integrity',p('Academic integrity is behaving in an honest, fair and responsible way in an academic setting. As a student at UWA India, you are part of a community that values academic integrity while studying at UWA India.')+p('Academic integrity requires acknowledging the contributions of other people when using their ideas to support your work. To display integrity shows others that you are honest and people can trust what you say, or in the case of assignments, that the work you submit has been completed by you unless you have indicated otherwise.')+p('Every UWA student is required to complete the Academic Conduct Essentials (ACE) and the Communication and Research Skills (CARS) modules. These modules outline the expectations of academic integrity while studying at UWA India.')+p('Your Learning Support Coordinator can support you to develop good academic practices in your note taking and writing, while Library & Learning Resource Advisor can support you with referencing. See the Learning Resources below and Library webpage.')),
 section('resources','Learning Resources',p('Explore a range of online resources that focus on key topics like academic integrity, writing and referencing, study techniques, planning and time management and more.')+actions([('library.html#library-guides','Library guides'),('lms.html','Access LMS information')])),
 section('workshops','Workshops and Individual Support',p('Academic Skills Workshops are available to help develop your writing, English, study skills and more.')+p('Your Learning Support Coordinator is also available for individual appointments with students to answer your questions and help guide you.')+button('contact.html','Request learning support'))
],source='PDF pages 10–11')
add('library','Library','Current students','Online collections, learning advice and quiet spaces for study.',[
 section('library-team','Your Library team',p('The University Library supports learning, teaching and research at UWA India. Library & Learning Resource Advisors at Mumbai and Chennai campuses are available to help all UWA India staff and students, with online support from Librarians at the University Library in Perth.')),
 section('online-collections','Online Collections',p("The Library manages Unit Readings. Students can access a list of their unit's readings, such as the unit’s essential textbook, from the Unit Readings link in their unit's Learning Management System (LMS). Essential textbooks for units can also be found on the Textbooks website in advance of LMS units opening.")+p("Through OneSearch, the Library provides all UWA staff and students with access to essential, relevant online academic resources, including full text articles, eBooks, and databases. UWA India staff and students have access to a selection of UWA Library's online resources that are relevant to the disciplines taught at UWA India.")+p('Sign in to OneSearch with your UWA UniID to ensure access to the full text of articles and ebooks, and to save items and searches to My Favourites.')+p("Improve the relevance of your search results in OneSearch by using the All Filters menu at the top of your search results. Use the 'Advanced Search' option to combine words and phrases in order to expand or narrow down your search.")+p('UWA India staff and postgraduate students can sign in to OneSearch to request digital scans of items from UWA Library’s physical collections, within the page limits permitted by Australian copyright law.')+actions([('https://onesearch.library.uwa.edu.au/discovery/search?vid=61UWA_INST%3AUWA','Open OneSearch'),('https://www.uwa.edu.au/library','UWA University Library')])),
 section('study-support','Study Support',p('Library and Learning Resource Advisors at UWA India are available to help students succeed in your learning. We can advise how to find academic information to use in your assignments, evaluate the quality of academic sources and how to reference correctly.')),
 section('library-guides','Library Guides',p('Library Guides provide quick, easy help with finding, using and referencing information.')+ul([link('https://guides.library.uwa.edu.au/UWAIndia','UWA India Library Guide'),'An Introduction to Referencing at UWA','Artificial Intelligence (AI)','EndNote referencing software','Referencing style – APA 7th','Referencing style – IEEE','Composing a Search','Ebooks','Company and industry information','Evaluating Information','Newspapers and news sources'])+button('https://guides.library.uwa.edu.au/','Browse UWA Library Guides')),
 section('ace-cars','ACE and CARS',p('ACE (Academic Conduct Essentials) and CARS (Communication and Research Skills) are two distinct compulsory units, that you are expected to complete in your first Semester or Trimester of study at UWA. They are designed to help you learn about academic integrity principles and to gain a strong grounding in basic study skills.')+p('Complete them both early in your studies, for a great head start to your studies. Look for them in your LMS.')+button('lms.html','LMS access and guidance')),
 section('referencing','Referencing',p("Referencing shows where you have used other people's ideas in your work and is an essential academic skill.")+p('Check out the Library guide “Referencing at UWA: A beginner’s guide” to find out about why you need to reference, how to manage your references, choosing the right style and getting help. Always use the referencing style recommended in your unit outline.')),
 section('individual-support','Individual study support',p('Library & Learning Resource Advisors can help you find information you need for your studies and answer any referencing questions. We can guide you in effectively using library resources and to develop your search techniques.')+p('Library & Learning Resource Advisors are available for individual appointments with students to support you.')+button('contact.html','Ask for Library support')),
 section('teaching-support','Teaching Support',p('Unit Coordinators can create and manage readings lists within the Unit Readings platform. More information for staff about Unit Readings is available on the Unit Readings Support Guide.')+p('Embed Library skills resources for your students in your LMS, from the collection of learning and teaching resources on the Library Information Literacy Skills Toolkit. Unit Coordinators are also very welcome to contact the Library to request support for students in their unit.')+p('See the UWA India staff Intranet for more information about Library services for staff.')+button('https://www.uwa.edu.au/library','Library services and resources')),
 section('research-support','Research Support',p('See the UWA India staff Intranet for forthcoming details about Library research services for staff.')),
 section('study-spaces','Library Study Spaces',p('UWA India’s Mumbai and Chennai campus libraries are quiet spaces for individual study. You’ll find a quiet, comfortable environment with a variety of seating available.')+p('Bring Your Own Device (BYOD) stations are available in the UWA India libraries. These stations consist of a monitor that you can plug your device into, to use as a second monitor via a USB-C connection which also charges your device.')+button('campus-facilities.html','Campus facilities'))
],source='PDF pages 11–14')
VIDEO='<iframe class="media-embed" src="https://player.vimeo.com/video/1133698349?autopause=1" title="Welcome To Blackboard Ultra – Student Video" loading="lazy" allow="fullscreen; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
add('lms','LMS','Current students','Your guide to the Blackboard Ultra Learning Management System.',[
 section('about-lms','Your online learning platform',p('The Blackboard Ultra Learning Management System (LMS) is the website where you’ll find all of the content for your units. It’s the digital platform where you:')+ul(['Receive unit information and announcements from your Unit Coordinator','Access the Unit Outline and weekly schedule for your unit','Access lecture slides and notes','Watch recorded lectures','Access your reading list','Submit assignments and get feedback','Join discussions with other students'])),
 section('access','Access the LMS',p('To access the LMS, we recommend using web browsers Google Chrome or Mozilla Firefox. You can also download and use the Blackboard App where you’ll find some useful guides.')+button('https://lms.uwa.edu.au/','Access the LMS')),
 section('navigation','Navigating Units',p('After accessing the LMS dashboard, locate and select your course from the Units tab. Note that the Content Page in each unit site includes a navigation menu horizontally across the top of the page and Unit Content in the centre.')+VIDEO),
 section('orientation','Blackboard Ultra Student Orientation',p('Watch the introductory video and self-enrol in our Blackboard Ultra Student Orientation site to learn more.')+'<ol><li>Log in to the Blackboard LMS.</li><li>Access the '+link('https://lms.uwa.edu.au/ultra/courses/_112355_1/outline','Student Orientation site')+'.</li><li>Select the “submit” button to enrol.</li></ol>'),
 section('materials','Learning Materials and Recordings',p('At UWA, content in the LMS is organised into modules according to week or topic. Click on the title of a Module to see the content for that week or topic, such as your Unit Coordinator’s instructions for the weekly tutorial, lecture notes, or practice questions.')+p('There is a dedicated section in your unit site called Unit Resources with links out to the full collection of lecture recordings for your unit and the full list of Unit Readings.')),
 section('grades','Viewing Grades and Feedback',p('When your Unit Coordinator releases grades for an assessment, grades will be visible in the LMS Grade Centre tab.')+p('Some assessment types might display your grade to you immediately, such as multiple-choice quizzes.')+p('For longer written assessment types, your Unit Coordinator will also provide feedback which you can view by clicking on the assessment title in Grade Centre.')),
 section('guides','LMS Guides and FAQs',p('Use the Student Orientation site above to learn more about Blackboard Ultra.')+resources([('https://help.blackboard.com/Learn/Student','Blackboard Learn for Students'),('https://www.youtube.com/user/BlackboardTV','Blackboard tutorials for students'),('faqs.html','UWA India FAQs')]))
],source='PDF pages 14–16')
fee_rows=''.join('<tr><th scope="row">'+link(c['url'],esc(c['name']))+'</th><td>₹'+c['domestic']+'</td><td>₹'+c['international']+'</td></tr>' for c in COURSES if c['domestic'])
add('fees','Fees','Study','Understand tuition fees and where to find the information for your course.',[
 section('published-fees','Published 2026 tuition fees',p('These published figures are for the first full year of study for students commencing in 2026. They are not whole-degree totals or confirmed prices for a later intake. Fees may change following annual review; additional charges may apply.')+'<div class="table-scroll" role="region" aria-label="Published tuition fees, scroll horizontally" tabindex="0"><table class="content-table"><thead><tr><th scope="col">Course</th><th scope="col">Domestic students (INR)</th><th scope="col">International students (INR)</th></tr></thead><tbody>'+fee_rows+'</tbody></table></div>'),
 section('confirm-fees','Confirm fees for your intake',p('Check the official course information and the fees in your offer before making study plans. Contact UWA India to confirm the applicable course, intake and student fee category.')+button('contact.html','Ask about course fees')),
 section('funding','Scholarships and support',p('Explore scholarship and financial support opportunities, with eligibility and availability published on individual scholarship pages.')+button('scholarships.html','Explore scholarships')),
 section('sources','Official course fee sources',resources([(c['source'],c['name']) for c in COURSES]))
],source='PDF page 8 requests existing website content; official course fee pages verified 11 November 2026')
add('english-language-requirements','English language requirements','Study','Find the English language information for your chosen course.',[
 section('requirements','Demonstrating English language competence',p('English is UWA’s teaching and assessment language. Approved qualifications or tests can demonstrate competence; some courses require higher results. Check your specific course requirements.')),
 section('tests','Common coursework test requirements','<div class="table-scroll" role="region" aria-label="English test requirements, scroll horizontally" tabindex="0"><table class="content-table"><thead><tr><th scope="col">Test</th><th scope="col">Standard coursework</th><th scope="col">Higher standard</th></tr></thead><tbody><tr><th scope="row">IELTS Academic</th><td>6.5 overall; 6.0 in each band</td><td>7.0 overall; 6.5 in each band</td></tr><tr><th scope="row">PTE Academic</th><td>64 overall; 60 in each band</td><td>70 overall; 64 in each band</td></tr></tbody></table></div>'+p('The UWA India MBA publishes the higher IELTS and PTE standard above. Approved test results normally have two-year validity.')),
 section('qualifications','Qualifications and other pathways',p('The official UWA page lists CBSE English at minimum B2 and CISCE English at minimum 60%, alongside other qualification and test pathways. Availability of English preparation pathways varies by course and cohort.')),
 section('check-course','Check the definitive requirements',p('Other tests, exemptions, course-specific rules and pathway conditions are available on UWA’s official requirements page. TOEFL requirements should be checked for your particular course.')+actions([(ENGLISH,'Official English language requirements'),('contact.html','Ask about your course')]))
],source='PDF page 8; official UWA English language requirements and UWA India MBA page, checked 11 November 2026')
add('careers','Work with UWA India','Careers','Explore employment opportunities with UWA India.',[
 section('work-with-us','Build your career with UWA India',p('Explore academic and professional opportunities supporting education, research and university operations in India. UWA India connects colleagues across campuses and encourages collaboration, inclusion and links with industry.')+button(INDIA+'work-with-uwa','View current vacancies')),
 section('applications','Applying for a role',p('Read the current advertisement for role requirements, location, application instructions and closing date. Use the contact listed in the advertisement when one is supplied.')+p('For recruitment enquiries, email '+link('mailto:uwaindia.talent@uwa.edu.au','uwaindia.talent@uwa.edu.au')+'.')),
 section('student-careers','Looking for student career support?',p('If you are a student seeking employability and career preparation resources, visit our student career support page.')+button('career-support.html','Student career support'))
],photo='join-uwa.jpg',source='PDF page 17; official UWA India Work with UWA page')
add('career-support','Career support','Current students','Prepare for your future career and build your employability.',[
 section('prepare','Career preparation',p('Explore support for employability, skill-building, gaining experience and preparing for career opportunities. UWA India’s official information identifies career coaching, industry mentors, CV and interview preparation, internships and networking.')+button(INDIA+'current-students/careers-support','Official student career support')),
 section('guidance','Find the right guidance',p('Contact our team for guidance on the career resources and activities available to you.')+actions([('contact.html','Contact student support'),('events.html','Events and networking')])),
 section('employment','Jobs at UWA India',p('Staff recruitment is separate from student career support.')+button('careers.html','Work with UWA India'))
],source='Official UWA India student careers-support page and course catalogue')
add('contact','Contact us','Contact us','Talk to our team about courses, applications, campuses and student support.',[
 section('enquiries','General enquiries',resources([('mailto:'+CONTACT_EMAIL,CONTACT_EMAIL),('tel:'+CONTACT_PHONE,'Call +91 79434 47630'),('https://wa.me/917200848304','WhatsApp +91 72008 48304')])+p('For an immediate emergency in India, call '+link('tel:112','112')+'.')),
 section('campuses','Our campuses',p('<strong>Mumbai</strong><br>'+MUMBAI)+p('<strong>Chennai</strong><br>'+CHENNAI)+actions([('campus-facilities.html','Campus facilities and maps')])),
 section('specialist','Specialist enquiries',resources([('mailto:scholarships.uwaindia@uwa.edu.au','Scholarships enquiries'),('mailto:student-wellbeing@india.uwa.edu.au','Student wellbeing (operating hours)'),('mailto:uwaindia.talent@uwa.edu.au','Staff recruitment')])+p('Wellbeing email is not an emergency service. For urgent danger in India, call 112.'))
],source='Official UWA India Contact us and wellbeing pages',form=True)
add('faqs','Frequently asked questions','How to apply','Find guidance on choosing a course, applying and getting support.',[section('questions','Your questions answered',faq_module())],source='Answers summarise supplied PDF pages 3–16')
add('policies','Policies and information','Policies','Find official University policies and information.',[
 section('official','Official policy and information links',p('Use the official University pages for the current policy wording and requirements.')+resources([('https://www.uwa.edu.au/privacy','Privacy'),('https://www.uwa.edu.au/terms-of-use','Terms of use'),('https://www.uwa.edu.au/accessibility','Accessibility')])),
 section('student-information','Student information',resources([('academic-support.html#academic-integrity','Academic integrity'),('library.html#referencing','Referencing'),('safety-on-campus.html','Campus safety and emergency information')]))
],source='PDF page 17 requests existing policy links')
add('search','Search UWA India','Search','Search courses, application guidance, campuses and student resources.',[
 section('page-search-results','Find a page','<form data-site-search role="search"><label for="page-search">Search the website</label><input class="filter-control" id="page-search" name="q" type="search" placeholder="For example: library, fees, Mumbai, computing" autocomplete="off"><button class="btn btn--primary" type="submit">Search</button></form><p id="search-status" role="status" aria-live="polite">Enter a word or phrase to find a page.</p><div class="search-results" id="search-results"></div>')
],source='Local site navigation feature')
for c in COURSES:
 overview=p(c['overview'])+'<dl class="course-facts"><dt>Level of study</dt><dd>'+c['level']+'</dd><dt>Campus</dt><dd>'+', '.join(c['campuses'])+'</dd><dt>Duration</dt><dd>'+c['duration']+'</dd></dl>'
 admission=p('Entry requirements depend on your course and qualifications. Check the official course page for the definitive academic and English language requirements, course structure and application information.')+actions([(c['source'],'Official course information'),('english-language-requirements.html','English language requirements')])
 fees=p('Check the published fee information for your course and confirm the amount that applies to your intake and student category. Scholarships have their own eligibility and availability conditions.')+actions([('fees.html','Fees'),('scholarships.html','Scholarships')])
 application=p('Check your eligibility, prepare your documents and submit your application directly or through an authorised UWA India education agent.')+actions([('how-to-apply.html','Application guide'),(APPLY,'Apply now')])
 add('course-'+c['slug'],c['name'],'Study',c['overview'],[section('overview','Course overview',overview),section('entry','Admission requirements',admission),section('fees','Fees and scholarships',fees),section('apply','How to apply',application)],photo='undergraduate-lab.jpg' if c['level']=='Undergraduate' else 'postgraduate-lab.jpg',source=c['source'])

GROUPS=[('Study',[('study.html','Study overview'),('why-uwa-india.html','Why UWA India'),('undergraduate-courses.html','Undergraduate courses'),('postgraduate-courses.html','Postgraduate courses'),('fees.html','Fees'),('scholarships.html','Scholarships'),('english-language-requirements.html','English language requirements')]),('How to apply',[('how-to-apply.html','Application guide'),('faqs.html','FAQs'),('contact.html','Contact us')]),('Student life',[('student-life.html','Student life overview'),('events.html','Events'),('safety-on-campus.html','Safety on campus'),('student-support-services.html','Student support services'),('campus-facilities.html','Campus facilities'),('campus-mumbai.html','Mumbai campus'),('campus-chennai.html','Chennai campus')]),('Current students',[('current-students.html','Current students overview'),('academic-support.html','Academic support'),('library.html','Library'),('lms.html','LMS'),('career-support.html','Career support')]),('Careers',[('careers.html','Work with UWA India')])]
def nav(filename):
 groups=''
 for label,items in GROUPS:
  opened=' open' if filename in [u for u,_ in items] else ''
  groups+=f'<li><details class="nav-group"{opened}><summary>{label}</summary><ul>'+''.join('<li><a href="'+u+'"'+(' aria-current="page"' if u==filename else '')+'>'+t+'</a></li>' for u,t in items)+'</ul></details></li>'
 return '<nav class="site-nav" id="site-nav" aria-label="Main"><ul class="container nav-groups"><li><a href="index.html"'+(' aria-current="page"' if filename in ['index.html','home.html'] else '')+'>Home</a></li>'+groups+'</ul></nav>'
def footer(title):
 f=FOOTER
 f=re.sub(r'<details class="footer-this-page">.*?</details>','<details class="footer-this-page"><summary>This page</summary><a href="#main-content">'+esc(title)+'</a></details>',f,flags=re.S)
 f=f.replace('Emergency<br>','Perth campus emergency<br>')
 f=f.replace('<p class="site-footer__cricos">','<p class="footer-location-note">For an emergency in India, call <a href="tel:112">112</a>. <a href="contact.html">UWA India enquiries</a>.</p><p class="site-footer__cricos">')
 f=f.replace('    </div>\n  </footer>','<nav class="footer-directory" aria-label="Footer navigation"><a href="site-map.html">All pages</a><a href="policies.html">Policies</a><a href="contact.html">Contact UWA India</a><a href="careers.html">Careers</a><a href="current-students.html">Current students</a><a href="faqs.html">FAQs</a></nav>\n    </div>\n  </footer>')
 return f

def render_page(page):
 filename=page['slug']+'.html';h=HEAD
 h=re.sub(r'<title>.*?</title>','<title>'+esc(page['title'])+' | UWA India</title>',h)
 h=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+esc(page['lead'])+'">',h)
 h=h.replace('assets/css/study.css','assets/css/site.css').replace('class="apply-page study-page"','class="apply-page document-page"')
 h=re.sub(r'<nav class="site-nav".*?</nav>',nav(filename),h,flags=re.S)
 h=h.replace('class="site-header__title">Study','class="site-header__title">'+esc(page['group']))
 group_link={'Study':'study.html','How to apply':'how-to-apply.html','Student life':'student-life.html','Current students':'current-students.html','Careers':'careers.html','Policies':'policies.html','Contact us':'contact.html','Search':'search.html'}[page['group']]
 crumbs='<ol class="container"><li><a href="index.html">UWA</a></li><li aria-hidden="true">›</li>'
 if group_link!=filename:crumbs+='<li><a href="'+group_link+'">'+page['group']+'</a></li><li aria-hidden="true">›</li>'
 crumbs+='<li aria-current="page">'+esc(page['title'])+'</li></ol>'
 h=re.sub(r'<ol class="container">.*?</ol>',crumbs,h,count=1,flags=re.S)
 photo=''
 if page['photo']:photo='<img class="document-hero__photo" src="assets/images/'+page['photo']+'" alt="'+({'career-students.jpg':'Students talking in a UWA campus garden','join-uwa.jpg':'The sandstone buildings and reflecting pool at UWA','campus-mumbai.jpg':'University campus setting','campus-chennai.jpg':'Students beneath sandstone campus arches','undergraduate-lab.jpg':'Students analysing data on laboratory monitors','postgraduate-lab.jpg':'Researchers reviewing laboratory data'}.get(page['photo'],'University campus'))+'" width="1200" height="600" fetchpriority="high">'
 hero='<section class="document-hero container"><p class="document-hero__eyebrow">'+esc(page['group'])+'</p><h1>'+esc(page['title'])+'</h1><p class="document-hero__lead">'+esc(page['lead'])+'</p>'+photo+'</section>'
 toc='<aside class="page-contents" aria-labelledby="contents-title"><h2 id="contents-title">On this page</h2><ul>'+''.join('<li><a href="#'+s['id']+'">'+esc(s['title'])+'</a></li>' for s in page['sections'])+'</ul></aside>'
 body=''.join('<section id="'+s['id']+'"><h2>'+esc(s['title'])+'</h2>'+s['body']+'</section>' for s in page['sections'])
 if page['form']:body+=enquiry()
 main='<main id="main-content" tabindex="-1">'+hero+'<div class="document-layout container">'+toc+'<article class="document-body" aria-label="'+esc(page['title'])+'">'+body+'</article></div>'+(contact_module() if page['slug'] not in ['contact','search'] else '')+'</main>'
 tail='<script src="assets/js/main.js"></script><script src="assets/js/search-index.js"></script><script src="assets/js/site.js"></script></body></html>'
 (ROOT/filename).write_text(h+main+footer(page['title'])+tail)

# A reviewable directory makes every screen reachable, including deeper support pages.
add('site-map','All pages','Study','Explore every page in the UWA India website.',[section('directory','Website directory',cards([('index.html','Homepage','Start exploring UWA India.'),('study.html','Study','Find your study pathway.'),('why-uwa-india.html','Why UWA India','Explore the UWA India experience.'),('undergraduate-courses.html','Undergraduate courses','Explore the undergraduate catalogue.'),('postgraduate-courses.html','Postgraduate courses','Explore the postgraduate catalogue.'),('how-to-apply.html','How to apply','Follow the application steps.'),('scholarships.html','Scholarships','Explore financial support opportunities.')])+cards([(p['slug']+'.html',p['title'],p['lead']) for p in PAGES if not p['slug'].startswith('course-')])+resources([(c['url'],c['name']) for c in COURSES]))],source='Website navigation')
for page in PAGES:render_page(page)
ARROW='<svg class="course-card__arrow" viewBox="0 0 24 20" aria-hidden="true"><path d="M2 10h19M14 3l7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
def catalogue(level=None):
 courses=[c for c in COURSES if not level or c['level']==level]
 level_select='<div><label>Level of study<select name="level" class="filter-control"><option value="">All levels</option><option>Undergraduate</option><option>Postgraduate</option></select></label></div>' if not level else ''
 filters='<form class="course-filter" data-course-filter role="search"><div><label>Search courses<input class="filter-control" name="q" type="search" placeholder="Search by course or study area"></label></div>'+level_select+'<div><label>Campus<select name="campus" class="filter-control"><option value="">All campuses</option><option>Mumbai</option><option>Chennai</option></select></label></div><button class="btn btn--outline" type="reset">Reset filters</button></form>'
 result='<div data-course-catalogue>'+filters+'<p class="course-count" role="status" aria-live="polite">'+str(len(courses))+' courses</p><div class="course-catalogue">'
 for i,c in enumerate(courses):
  picture=level=='Undergraduate' and i<2
  result+='<a class="course-card '+('course-card--image' if picture else 'course-card--text')+'" href="'+c['url']+'" data-catalogue-card data-title="'+esc(c['name']+' '+c['area'])+'" data-level="'+c['level']+'" data-campus="'+','.join(c['campuses'])+'">'
  if picture:result+='<img src="assets/images/join-uwa.jpg" alt="The UWA campus sandstone buildings" width="899" height="579" loading="lazy">'
  result+=('<span class="course-card__body">' if picture else '')+'<span><strong>'+esc(c['name'])+'</strong><small class="course-meta">'+esc(c['duration']+' · '+', '.join(c['campuses']))+'</small></span>'+ARROW+('</span>' if picture else '')+'</a>'
 return result+'</div><p class="course-empty" role="status" hidden>No courses match these filters. Try a different study area or campus.</p></div>'
# Existing screenshot screens are upgraded, not replaced by generic layouts.
EXISTING=['index.html','home.html','study.html','why-uwa-india.html','undergraduate-courses.html','postgraduate-courses.html','how-to-apply.html','scholarships.html']
for name in EXISTING:
 path=ROOT/name;s=path.read_text()
 s=re.sub(r'<link[^>]+(?:fonts.googleapis|fonts.gstatic)[^>]*>\s*','',s)
 if 'assets/css/how-to-apply.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="assets/css/how-to-apply.css">\n</head>')
 if 'assets/css/site.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="assets/css/site.css">\n</head>')
 s=re.sub(r'<nav class="site-nav".*?</nav>',nav(name),s,flags=re.S)
 s=s.replace('action="/search"','action="search.html"')
 if '<main>' in s:s=s.replace('<main>','<main id="main-content" tabindex="-1">',1)
 if name in ['index.html','home.html']:
  s=s.replace('<body id="top">','<body id="top" class="apply-page home-page">')
  if 'class="skip-link"' not in s:s=s.replace('<!-- SVG sprite -->','<a class="skip-link" href="#main-content">Skip to content</a>\n<!-- SVG sprite -->',1)
  s=re.sub(r'<section class="enquiry".*?</section>','<section class="enquiry container" id="register">'+enquiry('home-enquiry')+'</section>',s,flags=re.S)
  finder='<section class="study-section container" aria-labelledby="course-search-title"><h2 id="course-search-title">Find your course at UWA India</h2><form class="course-filter" action="study.html#courses" method="get" data-course-finder role="search"><label>Search by course or study area<input class="filter-control" name="q" type="search" placeholder="Business, computing, data…"></label><label>Level of study<select name="level" class="filter-control"><option value="">All levels</option><option>Undergraduate</option><option>Postgraduate</option></select></label><label>Campus<select name="campus" class="filter-control"><option value="">All campuses</option><option>Mumbai</option><option>Chennai</option></select></label><button class="btn btn--primary" type="submit">Find courses</button></form></section>'
  s=re.sub(r'<section class="section course-search".*?</section>',finder,s,flags=re.S)
  s=re.sub(r'\s*<script src="assets/js/form-data.js"></script>','',s)
 if name in ['undergraduate-courses.html','postgraduate-courses.html']:
  level='Undergraduate' if name.startswith('undergraduate') else 'Postgraduate'
  s=re.sub(r'<section class="course-list".*?</section>','<section class="course-list course-list--complete" aria-label="'+level+' courses" data-rendering="CourseListingCards">'+catalogue(level)+'</section>',s,flags=re.S)
  s=re.sub(r'\s*<dialog class="course-dialog".*?</dialog>','',s,flags=re.S)
  s=s.replace('<script src="assets/js/course-listings.js"></script>','')
 if name=='study.html':
  target='<section class="study-section container" id="courses"'
  start=s.find(target);end=s.find('</section>',start)
  if start!=-1 and 'data-course-catalogue' not in s[start:end]:s=s[:end]+catalogue()+s[end:]
 if name=='how-to-apply.html':
  s=s.replace('<button class="btn btn--ghost-white" type="button" data-open-faq>View FAQs</button>','<a class="btn btn--ghost-white" href="#application-faqs">View FAQs</a>')
  s=re.sub(r'<section class="connect container".*?</section>','<section class="container" id="application-faqs"><h2>Application FAQs</h2>'+faq_module(4)+button('faqs.html','View all FAQs')+'</section><div class="container">'+enquiry('application-enquiry')+'</div>',s,flags=re.S)
  s=re.sub(r'\s*<dialog class="faq-dialog".*?</dialog>','',s,flags=re.S)
  s=s.replace('<script src="assets/js/how-to-apply.js"></script>','')
 if name=='scholarships.html' and 'id="available-awards"' not in s:
  awards=[('early-bird-enrolment-bursary','Early Bird Enrolment Bursary','Automatic consideration'),('uwa-india-fee-waiver','UWA India Fee Waiver','Automatic consideration'),('tamil-nadu-uwa-bursary','Tamil Nadu UWA Bursary','Automatic consideration; campus and domicile conditions apply'),('maharashtra-uwa-bursary','Maharashtra UWA Bursary','Automatic consideration; campus and domicile conditions apply'),('premier-academic-award-maharashtra-tamil-nadu','Premier Academic Award (Maharashtra & Tamil Nadu)','Separate application'),('academic-merit-award','Academic Merit Award','Separate application'),('vice-chancellor-high-merit-award','Vice-Chancellor High-Merit Award','Separate application')]
  sectionhtml='<section class="study-section container" id="available-awards"><h2>Explore scholarships and bursaries</h2><p>Check each award’s eligibility and current availability. The separate-application award pages state that their 2026/27 applications are closed; no next-cycle opening date has been confirmed here.</p>'+cards([(INDIA+'scholarship/'+a,t,d+'. View eligibility and availability on the official award page.') for a,t,d in awards])+p('For scholarship enquiries, email '+link('mailto:scholarships.uwaindia@uwa.edu.au','scholarships.uwaindia@uwa.edu.au')+'.')+'</section>'
  s=s.replace('</main>',sectionhtml+'</main>',1)
 # Replace every original footer with the complete shared footer, retaining scripts.
 title=re.search(r'<title>(.*?)</title>',s).group(1).split('|')[0].strip()
 match=re.search(r'\s*<!-- ============ 13. Footer ============ -->.*?</footer>',s,re.S)
 if match:s=s[:match.start()]+footer(title)+s[match.end():]
 # Ensure all original screens expose the contact module without changing their hero composition.
 if name not in ['index.html','home.html','how-to-apply.html'] and 'id="shared-contact-title"' not in s:s=s.replace('</main>',contact_module()+'</main>',1)
 if 'assets/js/site.js' not in s:s=s.replace('</body>','<script src="assets/js/site.js"></script>\n</body>')
 # Correct old placeholder routes and links that previously returned to unrelated screens.
 mapping={'/':'index.html','/courses':'study.html#courses','/why-uwa-india':'why-uwa-india.html','/how-to-apply':'how-to-apply.html','/fees-and-scholarships':'fees.html','/student-life':'student-life.html','/campuses':'campus-facilities.html','/contact':'contact.html','/privacy-policy':'https://www.uwa.edu.au/privacy','/search':'search.html','/careers':'career-support.html','/campuses/mumbai':'campus-mumbai.html','/campuses/chennai':'campus-chennai.html','/scholarships':'scholarships.html','home.html#campuses':'campus-facilities.html'}
 for old,new in mapping.items():s=s.replace('href="'+old+'"','href="'+new+'"')
 s=s.replace('href="home.html">Student life','href="student-life.html">Student life').replace('href="home.html">Explore student life','href="student-life.html">Explore student life')
 s=s.replace('href="home.html#career-title"','href="career-support.html"')
 path.write_text(s)
# Shared search routes in newly generated pages, too.
for path in ROOT.glob('*.html'):
 s=path.read_text().replace('action="/search"','action="search.html"')
 s=s.replace('href="home.html#campuses"','href="campus-facilities.html"')
 path.write_text(re.sub(r'\n{3,}', '\n\n', '\n'.join(line.rstrip() for line in s.splitlines()))+'\n')
# Retain compatible catalogue option data without fabricated future intakes.
form_data={'campuses':{campus:{level:[c['name'] for c in COURSES if campus in c['campuses'] and c['level']==level] for level in ['Undergraduate','Postgraduate']} for campus in ['Mumbai','Chennai']},'intakes':[]}
(ROOT/'assets/js/form-data.js').write_text('/* Verified course options. Intake dates must be confirmed before being added. */\nwindow.UWA_FORM_DATA = '+json.dumps(form_data,indent=2)+';\n')
INDEX=[]
for path in sorted(ROOT.glob('*.html')):
 if path.name=='home.html':continue
 text=path.read_text(); title=re.search(r'<title>(.*?)</title>',text).group(1).split('|')[0].strip()
 desc=re.search(r'<meta name="description" content="(.*?)">',text)
 main=re.search(r'<main\b.*?</main>',text,re.S)
 content=html.unescape(re.sub(r'<[^>]+>',' ',main.group(0) if main else ''))
 INDEX.append({'url':path.name,'title':html.unescape(title),'description':html.unescape(desc.group(1)) if desc else '', 'content':re.sub(r'\s+',' ',content)[:16000]})
(ROOT/'assets/js/search-index.js').write_text('window.UWA_SEARCH_INDEX = '+json.dumps(INDEX,ensure_ascii=False)+';\n')
(ROOT/'assets/data/events.json').write_text(json.dumps([{'campus':'Mumbai','source':INDIA+'upcoming-events','type':'directory','confirmed_dates':None},{'campus':'Chennai','source':INDIA+'whats-new','type':'directory','confirmed_dates':None}],indent=2)+'\n')
coverage={'generated_pages':[{'page':p['slug']+'.html','title':p['title'],'source':p['source']} for p in PAGES], 'existing_pages':EXISTING,'content_gaps':['Campus-specific security numbers, assembly points and after-hours support require confirmation.','Official event listing dates conflict, so the local calendar has no asserted dates.','Enquiries prepare email drafts; no CRM or server submission is configured.','Existing scholarship and postgraduate photos may differ in crop from supplied screenshots.']}
(ROOT/'assets/data/content-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
print('Generated',len(PAGES),'new pages; upgraded',len(EXISTING),'existing pages;',len(INDEX),'searchable screens.')
