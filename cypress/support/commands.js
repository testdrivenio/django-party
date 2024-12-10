// cypress/support/commands.js

Cypress.Commands.add('login', () => {
    cy.session("logged-in-user", () => {
        const username = Cypress.env('username');
        const password = Cypress.env('password');

        cy.visit('/login/');
        cy.get('input[name="username"]').type(username);
        cy.get('input[name="password"]').type(password);
        cy.get('form').submit();
    }, {
        validate() {
            cy.document()
                .its('cookie')
                .should('contain', 'csrftoken');
        }
    });
});