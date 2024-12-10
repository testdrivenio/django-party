// cypress/e2e/e2e.cy.js

function fillAndSubmitPartyForm(party) {
    cy.get('input[name="party_date"]').clear().type(party.party_date);
    cy.get('input[name="party_time"]').clear().type(party.party_time);
    cy.get('input[name="venue"]').clear().type(party.venue);
    cy.get('textarea[name="invitation"]').clear().type(party.invitation);
    cy.get('form').submit();
}

function partyExistsOnPage(party) {
    cy.get('#party-invitation').should('contain', party.venue);
    cy.get('#party-invitation').should('contain', party.invitation);
}

function fillAndSubmitGiftForm(gift) {
    cy.get('input[name="gift"]').clear().type(gift.gift);
    cy.get('input[name="price"]').clear().type(gift.price);
    cy.get('input[name="link"]').clear().type(gift.gift_link);
    cy.get('form').submit();
}

function giftExistsOnPage(gift) {
    cy.get('#gift-registry').should('contain', gift.gift);
    cy.get('#gift-registry').should('contain', gift.price);
    cy.get('#gift-registry').should('contain', gift.gift_link);
}

function giftNotExistsOnPage(gift) {
    cy.get('#gift-registry').should('not.contain', gift.gift);
    cy.get('#gift-registry').should('not.contain', gift.price);
    cy.get('#gift-registry').should('not.contain', gift.gift_link);
}


function create_party() {
    cy.visit('/');
    cy.get('[data-cy="new-party-link"]').click();

    cy.fixture('party.json').then((party) => {
        fillAndSubmitPartyForm(party);
        cy.url().should('match', /\/party\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\/$/);
        partyExistsOnPage(party);
    });
}

function edit_party() {
    cy.get('[data-cy="edit-party-button"]').click();
    cy.fixture('updated_party.json').then((updated_party) => {
        fillAndSubmitPartyForm(updated_party);
        partyExistsOnPage(updated_party);
        cy.get('form').should('not.exist');
    });
}

function add_gift() {
    cy.visit('/');
    cy.get('[data-cy="gift-registry-link"]').first().click();

    cy.get('[data-cy="add-gift-button"]').click();
    cy.fixture('gift.json').then((gift) => {
        fillAndSubmitGiftForm(gift);
        cy.get('form').should('not.exist');
        giftExistsOnPage(gift);
    });
}

function edit_gift() {
    cy.get('[data-cy="edit-gift-button"]').first().click();
    cy.fixture('updated_gift.json').then((updated_gift) => {
        fillAndSubmitGiftForm(updated_gift);

        giftExistsOnPage(updated_gift);
        cy.get('form').should('not.exist');
    });
}

function delete_gift() {
    cy.get('[data-cy="delete-gift-button"]').first().click();
    cy.get('[data-cy="gift-removed-alert"]').should('be.visible');

    cy.fixture('updated_gift.json').then((updated_gift) => {
        giftNotExistsOnPage(updated_gift);
    });
}


describe('Logged in user creating and managing a party', () => {
    before(() => {
        cy.login();
    });

    it('Performs a complete party and gift registry workflow', function () {
        create_party();
        edit_party();
        add_gift();
        edit_gift();
        delete_gift();
    });
});