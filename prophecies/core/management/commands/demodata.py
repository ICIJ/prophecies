"""Generate a fictional dataset to demo Prophecies (screenshots, walkthroughs, tests).

The data is deliberately fake: the "Aurora Leaks" investigation, its checkers and
its records do not exist. Values are drawn with a fixed seed so two runs (and the
fixture generated from them) are identical.

Usage::

    python manage.py demodata
    python manage.py demodata --seed 7 --records 200
"""

import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from prophecies.core.models import (
    Choice,
    ChoiceGroup,
    Project,
    Task,
    TaskRecord,
    TaskRecordReview,
    Tip,
)

PROJECT_NAME = "Aurora Leaks"
PASSWORD = "demo"  # nosec: demo-only credentials

# (username, first name, last name, is_superuser)
CHECKERS = [
    ("demo", "Demo", "Admin", True),
    ("nadia", "Nadia", "Osei", False),
    ("tomas", "Tomás", "Vidal", False),
    ("lien", "Lien", "Nguyen", False),
    ("omar", "Omar", "Haddad", False),
]

COUNTRIES = [
    ("Panama", "PAN", "Calle 50, Torre Global, Panama City"),
    ("Seychelles", "SYC", "Suite 8, Global Village, Victoria, Mahé"),
    ("Cyprus", "CYP", "12 Arch. Makariou III, Nicosia"),
    ("Malta", "MLT", "Level 3, Quantum House, Valletta"),
    ("Singapore", "SGP", "8 Marina View, Asia Square Tower 1"),
    ("Uruguay", "URY", "Rincón 487, Ciudad Vieja, Montevideo"),
    ("Cook Islands", "COK", "PO Box 3017, Avarua, Rarotonga"),
    ("Belize", "BLZ", "35 Barrack Road, Belize City"),
]

COMPANY_PARTS = (
    ["Aurora", "Northwind", "Blue Harbour", "Silverkeep", "Delta Crest", "Kestrel"],
    ["Holdings", "Trading", "Capital", "Ventures", "Management", "Investments"],
    ["Ltd", "S.A.", "Inc", "Corp", "LLC"],
)

PEOPLE = (
    ["Marta", "Ivan", "Chiara", "Kwame", "Lucía", "Anders", "Priya", "Yusuf"],
    ["Lindqvist", "Oyelaran", "Ferrari", "Novak", "Ibrahim", "Costa", "Nakamura"],
)

TIPS = [
    (
        "Spotting a nominee director",
        "A director sitting on **dozens** of unrelated companies at the same "
        "registered address is usually a nominee, not a decision maker.",
    ),
    (
        "Jurisdiction vs. address",
        "The registered address is not always in the jurisdiction of "
        "incorporation. Check the incorporation document before flagging a "
        "mismatch as an error.",
    ),
    (
        "When in doubt, leave a note",
        "Use `@username` in a note to pull a colleague into a record you are "
        "unsure about instead of guessing.",
    ),
]


def _messy(rng, value):
    """Return `value` the way a real dataset would hold it: noisy and uneven."""
    tweaks = [str.upper, str.lower, lambda v: f"  {v} ", lambda v: v.replace(" ", "  "), lambda v: v]
    return rng.choice(tweaks)(value)


class Command(BaseCommand):
    help = "Create a fictional project, tasks, records and reviews for demos."

    def add_arguments(self, parser):
        parser.add_argument("--seed", type=int, default=42, help="Random seed.")
        parser.add_argument(
            "--records", type=int, default=120, help="Records per task."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(options["seed"])
        # Re-runnable: wipe the previous demo dataset, keep everything else
        Project.objects.filter(name=PROJECT_NAME).delete()
        User.objects.filter(username__in=[c[0] for c in CHECKERS]).delete()

        users = []
        for username, first_name, last_name, is_superuser in CHECKERS:
            user = User.objects.create_user(
                username,
                email=f"{username}@example.org",
                password=PASSWORD,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_superuser,
                is_superuser=is_superuser,
            )
            users.append(user)
        admin = users[0]
        # Everyone checks, the admin included, so a demo session logged in as
        # "demo" sees the tasks in the app and not just in the admin.
        project = Project.objects.create(name=PROJECT_NAME, creator=admin)
        tasks = [
            self.create_task(project, admin, users, spec)
            for spec in self.task_specs()
        ]

        for task in tasks:
            self.create_records(rng, task, options["records"])
            self.create_reviews(rng, task)

        for name, description in TIPS:
            Tip.objects.create(
                name=name,
                description=description,
                project=project,
                task=rng.choice(tasks),
                creator=admin,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Created "{PROJECT_NAME}" with {len(tasks)} tasks, '
                f'{TaskRecord.objects.filter(task__project=project).count()} records, '
                f"{len(users)} users (password: {PASSWORD})."
            )
        )

    def task_specs(self):
        """Yield (task kwargs, choices) pairs, one per demo task."""
        return [
            (
                dict(
                    name="Company jurisdictions",
                    description="Is the predicted country of incorporation right?",
                    rounds=2,
                    color="#31807D",
                ),
                "Is the country correct?",
                [
                    ("Correct", "#0b8f3a", "c", False),
                    ("Incorrect", "#c0392b", "i", True),
                    ("Unclear", "#e6a700", "u", False),
                ],
            ),
            (
                dict(
                    name="Officer names",
                    description="Check the spelling of each officer name.",
                    rounds=3,
                    color="#a4287d",
                ),
                "Name check",
                [
                    ("Correct", "#0b8f3a", "c", False),
                    ("Misspelled", "#c0392b", "m", True),
                    ("Duplicate", "#8e44ad", "d", False),
                    ("Not a person", "#7f8c8d", "n", False),
                ],
            ),
            (
                dict(
                    name="Registered addresses",
                    description="Is this address usable as-is?",
                    rounds=1,
                    color="#1f6fb2",
                ),
                "Address quality",
                [
                    ("Valid", "#0b8f3a", "v", False),
                    ("Incomplete", "#e6a700", "p", True),
                    ("Junk", "#c0392b", "j", False),
                ],
            ),
        ]

    def create_task(self, project, creator, checkers, spec):
        task_kwargs, choice_group_name, choices = spec
        choice_group = ChoiceGroup.objects.create(name=choice_group_name)
        for name, color, shortkeys, require_alternative_value in choices:
            Choice.objects.create(
                choice_group=choice_group,
                name=name,
                value=name.lower().replace(" ", "-"),
                color=color,
                shortkeys=shortkeys,
                require_alternative_value=require_alternative_value,
            )
        task = Task.objects.create(
            project=project,
            creator=creator,
            choice_group=choice_group,
            **task_kwargs,
        )
        task.checkers.set(checkers)
        return task

    def create_records(self, rng, task, count):
        for i in range(count):
            country, code, address = rng.choice(COUNTRIES)
            if task.name == "Company jurisdictions":
                company = " ".join(rng.choice(part) for part in COMPANY_PARTS)
                original, predicted = _messy(rng, f"{company}, {address}"), country
            elif task.name == "Officer names":
                first, last = (rng.choice(part) for part in PEOPLE)
                original, predicted = _messy(rng, f"{last}, {first}"), f"{first} {last}"
            else:
                original, predicted = _messy(rng, address), f"{address}, {country}"
            TaskRecord.objects.create(
                task=task,
                uid=f"{task.id}-{i:04d}",
                original_value=original,
                predicted_value=predicted,
                metadata={"country_code": code, "source_row": i + 2},
                priority=rng.choice([1, 1, 1, 2, 3]),
            )

    def create_reviews(self, rng, task):
        """Assign every record to `task.rounds` checkers and review most of them."""
        choices = list(task.choice_group.choices.all())
        checkers = list(task.checkers.all())
        for record in task.records.all():
            for checker in rng.sample(checkers, task.rounds):
                review = TaskRecordReview(task_record=record, checker=checker)
                if rng.random() < 0.65:  # the rest stays pending, for the progress bars
                    review.choice = rng.choice(choices)
                    if review.choice.require_alternative_value:
                        review.alternative_value = record.predicted_value.title()
                    if rng.random() < 0.06:
                        review.note = rng.choice(
                            [
                                "Two companies share this address — worth a second look.",
                                "@nadia can you confirm the registry spelling here?",
                                "Source document is unreadable for this row.",
                                "@demo please double-check before we close this round.",
                            ]
                        )
                review.save()
