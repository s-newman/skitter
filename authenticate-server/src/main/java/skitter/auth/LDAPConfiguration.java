package skitter.auth;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.ldap.core.LdapTemplate;
import org.springframework.ldap.core.support.LdapContextSource;

@Configuration
public class LDAPConfiguration {

    private String username = "";
    private String password = "";

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Bean
    public LdapContextSource contextSource() {
        LdapContextSource contextSource = new LdapContextSource();
        contextSource.setUrl("ldaps://ldap.rit.edu:636");
        contextSource.setUserDn(this.username);
        contextSource.setPassword(this.password);
        contextSource.afterPropertiesSet();
        return contextSource;
    }

    @Bean
    public LdapTemplate ldapTemplate() {
        LdapContextSource ctx = contextSource();

        LdapTemplate ldapTemplate = new LdapTemplate(ctx);
        try {
            ldapTemplate.afterPropertiesSet();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ldapTemplate;
    }
}
