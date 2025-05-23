from widgetastic.widget import Checkbox, Text, TextInput, View
from widgetastic_patternfly5 import Button, Pagination as PF5Pagination
from widgetastic_patternfly5.ouia import Dropdown, Modal, PatternflyTable, Switch

from airgun.views.common import BaseLoggedInView, SearchableViewMixinPF4


class CloudTokenView(BaseLoggedInView):
    """Insights Landing page for adding RH Cloud Token."""

    rhcloud_token = TextInput(locator='//input[contains(@aria-label, "input-cloud-token")]')
    save_token = Button('Save setting and sync recommendations')

    @property
    def is_displayed(self):
        return self.rhcloud_token.wait_displayed()


class RemediationView(Modal):
    """Insights Remediations modal view"""

    OUIA_ID = 'OUIA-Generated-Modal-large-1'
    remediate = Button('Remediate')
    cancel = Button('Cancel')
    table = PatternflyTable(
        component_id='OUIA-Generated-Table-2',
        column_widgets={
            'Hostname': Text('./a'),
            'Recommendation': Text('./a'),
            'Resolution': Text('.//a'),
            'Reboot Required': Text('.//a'),
        },
    )

    @property
    def is_displayed(self):
        return self.title.wait_displayed()


class CloudInsightsView(BaseLoggedInView, SearchableViewMixinPF4):
    """Main Insights view."""

    title = Text('//h1[normalize-space(.)="Red Hat Insights"]')
    insights_sync_switcher = Switch('OUIA-Generated-Switch-1')
    remediate = Button('Remediate')
    insights_dropdown = Dropdown('OUIA-Generated-Dropdown-2')
    select_all = Checkbox(locator='.//input[@aria-label="Select all rows"]')
    table = PatternflyTable(
        component_id='OUIA-Generated-Table-2',
        column_widgets={
            0: Checkbox(locator='.//input[@type="checkbox"]'),
            'Hostname': Text('.//a'),
            'Recommendation': Text('.//a'),
            'Total Risk': Text('.//a'),
            'Playbook': Text('.//a'),
        },
    )
    select_all_hits = Button('Select recommendations from all pages')
    clear_hits_selection = Button('Clear Selection')
    pagination = PF5Pagination()
    remediation_window = View.nested(RemediationView)

    @property
    def is_displayed(self):
        return self.browser.wait_for_element(self.title, exception=False) is not None
