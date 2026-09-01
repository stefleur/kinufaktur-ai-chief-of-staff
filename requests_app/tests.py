from django.test import TestCase
from django.urls import reverse

from .models import BusinessRequest


class BusinessRequestModelTests(TestCase):
    def test_new_request_has_expected_defaults(self):
        business_request = BusinessRequest.objects.create(
            title="Automate invoices",
            description="Reduce manual invoice processing.",
        )

        self.assertEqual(business_request.category, BusinessRequest.Category.OTHER)
        self.assertEqual(business_request.status, BusinessRequest.Status.NEW)
        self.assertEqual(business_request.action_plan, "")
        self.assertEqual(str(business_request), "Automate invoices")


class BusinessRequestViewTests(TestCase):
    def setUp(self):
        self.business_request = BusinessRequest.objects.create(
            title="Consolidate customer data",
            description="Create a single source of truth.",
        )

    def test_list_displays_existing_requests(self):
        response = self.client.get(reverse("requests_app:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.business_request.title)

    def test_create_page_displays_form(self):
        response = self.client.get(reverse("requests_app:create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New business request")

    def test_valid_intake_creates_request_and_redirects_to_detail(self):
        response = self.client.post(
            reverse("requests_app:create"),
            {"title": "Build AI support", "description": "Triage support tickets."},
        )
        created = BusinessRequest.objects.get(title="Build AI support")

        self.assertRedirects(
            response,
            reverse("requests_app:detail", args=[created.pk]),
        )

    def test_invalid_intake_does_not_create_request(self):
        response = self.client.post(
            reverse("requests_app:create"),
            {"title": "", "description": "Missing title."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "title", "This field is required.")
        self.assertEqual(BusinessRequest.objects.count(), 1)

    def test_detail_displays_workflow_information(self):
        response = self.client.get(
            reverse("requests_app:detail", args=[self.business_request.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Consolidate customer data")
        self.assertContains(response, "Other")
        self.assertContains(response, "New")

    def test_missing_request_returns_404(self):
        response = self.client.get(reverse("requests_app:detail", args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_workflow_update_persists_changes(self):
        response = self.client.post(
            reverse("requests_app:update", args=[self.business_request.pk]),
            {
                "category": BusinessRequest.Category.DATA,
                "action_plan": "Audit sources, then define the canonical schema.",
                "status": BusinessRequest.Status.PLANNED,
            },
        )
        self.business_request.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("requests_app:detail", args=[self.business_request.pk]),
        )
        self.assertEqual(self.business_request.category, BusinessRequest.Category.DATA)
        self.assertEqual(self.business_request.status, BusinessRequest.Status.PLANNED)
        self.assertIn("Audit sources", self.business_request.action_plan)

# Create your tests here.
